"""
Smart Dash / asistente heurístico de cartera.

Este router nunca había existido en el repo (huérfano: el frontend y
gestor_tools.py ya lo referenciaban) pese a que la capa de datos duros
(src/core/smart_dash.py) estaba completa. Acá se agrega la capa que faltaba:
señales por cuenta, score de prioridad, plan de pago sugerido, compliance
de horario, y la generación de mensajes vía Hermes (LLM).

Las reglas de scoring/plan de pago/horario son heurísticas razonables y
documentadas en el código, pensadas para ajustarse fácilmente una vez que
el equipo de cobranza las valide contra su criterio real de negocio.
"""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.auth_database import get_auth_db
from src.core.security import get_current_user
from src.core import smart_dash
from src.core.hermes_client import chat as hermes_chat
from src.models.cuentas import Cuenta, Entidad
from src.models.contactos import Contacto
from src.models.catalogos import Resultado
from src.models.financiero import Convenio, Vencimiento, Cobro
from src.models.usuario import Usuario

router = APIRouter(prefix="/asistente", tags=["Asistente IA"])

TZ_AR = ZoneInfo("America/Argentina/Buenos_Aires")
HORARIO_DESDE, HORARIO_HASTA = 8, 20  # horario habitual de contacto (ver system prompt de gestor_tools.py)


# ============================================================================
# Señales por cuenta (usado por priorización, estrategia y el dossier del
# gestor IA). Batcheado: recibe una lista de id_cta y resuelve todo con
# pocas queries, sin N+1.
# ============================================================================

def _señales_batch(db: Session, id_ctas: list[int]) -> dict[int, dict]:
    if not id_ctas:
        return {}

    hoy = date.today()
    cuentas = {c.id_cta: c for c in db.query(Cuenta).filter(Cuenta.id_cta.in_(id_ctas)).all()}

    # Gestiones: total y sin resultado registrado, por cuenta (dos queries
    # agregadas simples en vez de un CASE WHEN, para no atarse a un dialecto).
    gestiones_totales = dict(
        db.query(Contacto.cuentas_id_cta, func.count(Contacto.id_contacto))
        .filter(Contacto.cuentas_id_cta.in_(id_ctas), Contacto.activo == "S")
        .group_by(Contacto.cuentas_id_cta)
        .all()
    )
    gestiones_sin_resultado = dict(
        db.query(Contacto.cuentas_id_cta, func.count(Contacto.id_contacto))
        .filter(
            Contacto.cuentas_id_cta.in_(id_ctas),
            Contacto.activo == "S",
            Contacto.resultados_id_resultado.is_(None),
        )
        .group_by(Contacto.cuentas_id_cta)
        .all()
    )

    # Promesa incumplida: último contacto con resultado "compromiso...", de
    # hace más de 7 días, sin ningún cobro registrado desde esa fecha.
    compromisos = (
        db.query(Contacto.cuentas_id_cta, func.max(Contacto.fecha_contacto))
        .join(Resultado, Contacto.resultados_id_resultado == Resultado.id_resultado)
        .filter(
            Contacto.cuentas_id_cta.in_(id_ctas),
            Contacto.activo == "S",
            Resultado.desc_resultado.ilike("%compromiso%"),
        )
        .group_by(Contacto.cuentas_id_cta)
        .all()
    )
    ultimos_cobros = dict(
        db.query(Cobro.cuentas_id_cta, func.max(Cobro.fcha_cobro))
        .filter(
            Cobro.cuentas_id_cta.in_(id_ctas),
            (Cobro.anulado.is_(None)) | (Cobro.anulado != "S"),
        )
        .group_by(Cobro.cuentas_id_cta)
        .all()
    )
    promesa_incumplida: dict[int, bool] = {}
    for id_cta, fecha_compromiso in compromisos:
        if not fecha_compromiso or (hoy - fecha_compromiso).days < 7:
            continue
        ultimo_cobro = ultimos_cobros.get(id_cta)
        promesa_incumplida[id_cta] = not ultimo_cobro or ultimo_cobro < fecha_compromiso

    # Convenio caído: convenio no cancelado con al menos una cuota vencida
    # (fecha < hoy) todavía impaga.
    convenios_vigentes = (
        db.query(Convenio.id_convenios, Convenio.cuentas_id_cta)
        .filter(Convenio.cuentas_id_cta.in_(id_ctas), Convenio.cancelado != "S")
        .all()
    )
    convenio_por_id = {c.id_convenios: c.cuentas_id_cta for c in convenios_vigentes}
    convenio_caido: dict[int, bool] = {}
    if convenio_por_id:
        vencidos = (
            db.query(Vencimiento.id_convenio)
            .filter(
                Vencimiento.id_convenio.in_(convenio_por_id.keys()),
                Vencimiento.pagado == "N",
                Vencimiento.fecha < hoy,
            )
            .distinct()
            .all()
        )
        for (id_convenio,) in vencidos:
            id_cta = convenio_por_id.get(id_convenio)
            if id_cta is not None:
                convenio_caido[id_cta] = True

    resultado = {}
    for id_cta in id_ctas:
        cuenta = cuentas.get(id_cta)
        antiguedad = (hoy - cuenta.fechaingreso_cta).days if cuenta and cuenta.fechaingreso_cta else 0
        resultado[id_cta] = {
            "antiguedad_dias": max(antiguedad, 0),
            "judicial_activa": bool(cuenta and cuenta.judicial == "S"),
            "gestiones_previas": int(gestiones_totales.get(id_cta, 0)),
            "gestiones_sin_resultado": int(gestiones_sin_resultado.get(id_cta, 0)),
            "promesa_incumplida": bool(promesa_incumplida.get(id_cta, False)),
            "convenio_caido": bool(convenio_caido.get(id_cta, False)),
        }
    return resultado


# ============================================================================
# Score de prioridad y plan de pago sugerido
# ============================================================================

def _score_prioridad(deuda: float, deuda_max: float, señales: dict) -> int:
    """0-100. Pesos heurísticos: antigüedad y deuda relativa aportan gradualmente,
    las señales duras (judicial, convenio caído, promesa incumplida) suman fijo."""
    score = 0.0
    score += min(señales["antiguedad_dias"] / 30, 12) * 2.5  # hasta 30 pts por antigüedad (12 meses)
    if deuda_max > 0:
        score += min(deuda / deuda_max, 1) * 20  # hasta 20 pts por peso relativo de la deuda
    score += 25 if señales["judicial_activa"] else 0
    score += 20 if señales["convenio_caido"] else 0
    score += 15 if señales["promesa_incumplida"] else 0
    score += min(señales["gestiones_sin_resultado"], 5) * 2  # hasta 10 pts
    return round(min(score, 100))


def _nivel_prioridad(score: int) -> str:
    if score >= 70:
        return "ALTA"
    if score >= 40:
        return "MEDIA"
    return "BAJA"


def _plan_sugerido(deuda: float) -> dict:
    """Cuotas/anticipo por tramo de deuda. Redondeado a centenas para que sea
    un número "ofrecible" en una negociación real."""
    if deuda <= 50_000:
        cant_cuotas = 3
    elif deuda <= 200_000:
        cant_cuotas = 6
    else:
        cant_cuotas = 12
    anticipo = round(deuda * 0.20, -2)
    importe_cuota = round(max(deuda - anticipo, 0) / cant_cuotas, -2) if cant_cuotas else 0
    return {"cant_cuotas": cant_cuotas, "importe_cuota": importe_cuota, "anticipo_sugerido": anticipo}


def _proxima_accion(señales: dict) -> str:
    if señales["judicial_activa"]:
        return "Cuenta en instancia judicial: coordinar seguimiento con el estudio antes de re-contactar."
    if señales["convenio_caido"]:
        return "Convenio caído: contactar para regularizar o renegociar el plan de pago."
    if señales["promesa_incumplida"]:
        return "Promesa de pago incumplida: reclamar cumplimiento o reprogramar el compromiso."
    if señales["gestiones_sin_resultado"] >= 3:
        return "Varias gestiones sin resultado: probar un canal distinto (WhatsApp, visita) o cambiar de gestor."
    if señales["gestiones_previas"] == 0:
        return "Sin gestiones registradas todavía: realizar el primer contacto."
    return "Continuar seguimiento de rutina."


def _compliance_horario(db: Session, id_cta: int) -> dict:
    ahora = datetime.now(TZ_AR)
    horario_ok = HORARIO_DESDE <= ahora.hour < HORARIO_HASTA
    motivo = None if horario_ok else f"Fuera del horario habitual de contacto ({HORARIO_DESDE:02d}:00–{HORARIO_HASTA:02d}:00)."

    ya_contactado_hoy = (
        db.query(Contacto)
        .filter(Contacto.cuentas_id_cta == id_cta, Contacto.activo == "S", Contacto.fecha_contacto == ahora.date())
        .first()
        is not None
    )
    return {"horario_ok": horario_ok, "motivo": motivo, "ya_contactado_hoy": ya_contactado_hoy}


def _nombre_y_deuda(cuenta: Cuenta, db: Session) -> tuple[str, float]:
    entidad = db.query(Entidad).filter(Entidad.matricula_ent == cuenta.entidades_matricula_ent).first()
    return (entidad.razon_social_ent if entidad else "—", float(cuenta.deudaact_cta or 0))


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/smart_dash")
def smart_dash_endpoint(
    dias: int = Query(90, ge=1, le=730),
    desde: date | None = Query(None),
    hasta: date | None = Query(None),
    subcliente_id: int | None = Query(None),
    estado_id: int | None = Query(None),
    usuario_id: int | None = Query(None),
    db: Session = Depends(get_db),
    auth_db: Session = Depends(get_auth_db),
    _user: dict = Depends(get_current_user),
):
    hasta_ = hasta or date.today()
    desde_ = desde or (hasta_ - timedelta(days=dias))

    datos = smart_dash.minar_todo(db, desde_, hasta_, subcliente_id, estado_id, usuario_id)

    # top_gestores viene como {usuario_id, cant} (ver smart_dash.minar_gestion):
    # se resuelve el nombre acá, contra la DB de auth.
    top = datos["gestion"]["top_gestores"]
    ids = [g["usuario_id"] for g in top]
    nombres = {}
    if ids:
        nombres = dict(auth_db.query(Usuario.id_usuario, Usuario.loguin_usuario).filter(Usuario.id_usuario.in_(ids)).all())
    datos["gestion"]["top_gestores"] = [{"nombre": nombres.get(g["usuario_id"], "—"), "cant": g["cant"]} for g in top]

    hallazgos = smart_dash.generar_hallazgos(datos)
    filtros = {
        "alcance": "Cartera filtrada" if (subcliente_id or estado_id or usuario_id) else "Cartera completa",
        "periodo": f"{desde_.isoformat()} a {hasta_.isoformat()}",
    }
    narrativa = smart_dash.generar_narrativa(datos, hallazgos, filtros)

    return {"data": {**datos, "hallazgos": hallazgos, "narrativa": narrativa}}


@router.get("/priorizar_contactos")
def priorizar_contactos(
    limite: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    # Pool de candidatas: activas, ordenadas por deuda desc, acotado para no
    # calcular señales sobre toda la cartera en cada request.
    pool = (
        db.query(Cuenta)
        .filter(Cuenta.activa_cta == "S")
        .order_by(Cuenta.deudaact_cta.desc())
        .limit(300)
        .all()
    )
    if not pool:
        return {"data": []}

    id_ctas = [c.id_cta for c in pool]
    señales_map = _señales_batch(db, id_ctas)
    deuda_max = max((float(c.deudaact_cta or 0) for c in pool), default=0.0)

    items = []
    for c in pool:
        nombre, deuda = _nombre_y_deuda(c, db)
        señales = señales_map.get(c.id_cta, {})
        score = _score_prioridad(deuda, deuda_max, señales)
        items.append({
            "id_cta": c.id_cta,
            "nombre": nombre,
            "deuda": deuda,
            "score_prioridad": score,
            "nivel_prioridad": _nivel_prioridad(score),
            "señales": {
                "judicial_activa": señales.get("judicial_activa", False),
                "convenio_caido": señales.get("convenio_caido", False),
                "promesa_incumplida": señales.get("promesa_incumplida", False),
            },
        })

    items.sort(key=lambda x: x["score_prioridad"], reverse=True)
    return {"data": items[:limite]}


@router.get("/estrategia/{id_cta}")
def estrategia_cuenta(
    id_cta: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    cuenta = db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail=f"Cuenta {id_cta} no encontrada")

    nombre, deuda = _nombre_y_deuda(cuenta, db)
    señales_completas = _señales_batch(db, [id_cta])[id_cta]

    deuda_max = db.query(func.max(Cuenta.deudaact_cta)).filter(Cuenta.activa_cta == "S").scalar()
    deuda_max = float(deuda_max or deuda or 1)
    score = _score_prioridad(deuda, deuda_max, señales_completas)

    return {"data": {
        "id_cta": cuenta.id_cta,
        "nombre": nombre,
        "deuda": deuda,
        "score_prioridad": score,
        "nivel_prioridad": _nivel_prioridad(score),
        "señales": señales_completas,
        "compliance": _compliance_horario(db, id_cta),
        "plan_sugerido": _plan_sugerido(deuda),
        "proxima_accion": _proxima_accion(señales_completas),
    }}


@router.get("/recomendaciones")
def recomendaciones(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Recomendaciones de cartera: mismo motor de hallazgos de Smart Dash
    (últimos 90 días, cartera completa), en formato de lista accionable."""
    hasta = date.today()
    desde = hasta - timedelta(days=90)
    datos = smart_dash.minar_todo(db, desde, hasta)
    hallazgos = smart_dash.generar_hallazgos(datos)

    items = [{"titulo": h["titulo"], "detalle": h["detalle"]} for h in hallazgos if h["nivel"] in ("critico", "atencion")]
    return {"data": items}


class GenerarMensajeIn(BaseModel):
    id_cta: int
    tipo: str  # PRIMER_CONTACTO | RECORDATORIO | NEGOCIACION | FINAL
    tono: str  # profesional | cordial | urgente | empatico


_TIPO_DESC = {
    "PRIMER_CONTACTO": "un primer contacto con el deudor, presentando la gestión",
    "RECORDATORIO": "un recordatorio de pago pendiente",
    "NEGOCIACION": "una propuesta de plan de pago para negociar la deuda",
    "FINAL": "un último aviso antes de escalar la gestión",
}


@router.post("/generar_mensaje")
def generar_mensaje(
    payload: GenerarMensajeIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    cuenta = db.query(Cuenta).filter(Cuenta.id_cta == payload.id_cta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail=f"Cuenta {payload.id_cta} no encontrada")

    nombre, deuda = _nombre_y_deuda(cuenta, db)
    plan = _plan_sugerido(deuda)
    compliance = _compliance_horario(db, payload.id_cta)
    tipo_desc = _TIPO_DESC.get(payload.tipo, "un mensaje de gestión de cobranza")

    prompt = (
        f"Redactá {tipo_desc} para WhatsApp, en tono {payload.tono}, dirigido a {nombre}. "
        f"Deuda actual: $ {deuda:,.0f}. Plan sugerido si negocia: {plan['cant_cuotas']} cuotas de "
        f"$ {plan['importe_cuota']:,.0f} con anticipo de $ {plan['anticipo_sugerido']:,.0f}. "
        "Máximo 4 líneas, sin firmar con nombre de persona, profesional y directo, "
        "en español rioplatense. No inventes datos que no te di."
    ).replace(",", ".")

    respuesta = hermes_chat([
        {"role": "system", "content": "Sos un asistente de redacción para gestores de cobranza extrajudicial."},
        {"role": "user", "content": prompt},
    ])

    mensaje = respuesta.get("content") or ""
    advertencia = None
    if respuesta.get("error"):
        advertencia = "No se pudo generar el mensaje con IA; revisá la configuración de Hermes."
    elif respuesta.get("simulado"):
        advertencia = "Hermes no está configurado (HERMES_API_URL): mensaje de prueba, no generado por IA real."
    elif not compliance["horario_ok"]:
        advertencia = compliance["motivo"]

    return {"data": {"mensaje": mensaje, "plan_sugerido": plan, "advertencia": advertencia}}
