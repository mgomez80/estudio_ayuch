"""Smart Dash: minería de patrones de cartera + motor de hallazgos por reglas.

Capa 1 (Task 2): funciones minar_* que consultan la DB con filtros.
Capa 2 (esta): reglas puras que convierten lo minado en hallazgos y narrativa.
Sin LLM: el "análisis" es determinístico y auditable.
"""

from datetime import date, timedelta

from sqlalchemy import Numeric, cast, func

from src.models.catalogos import Accion, Resultado
from src.models.contactos import Contacto
from src.models.cuentas import Cuenta
from src.models.financiero import Cobro

# La deuda se guarda como VARCHAR; casteamos para agregaciones (patrón asistente.py).
DEUDA_NUM = cast(Cuenta.deudaact_cta, Numeric(20, 2))

_BUCKETS = [("0-30", 0, 30), ("31-90", 31, 90), ("91-180", 91, 180), ("+180", 181, None)]


def _cuentas_filtradas(db, subcliente_id=None, estado_id=None):
    q = db.query(Cuenta).filter(Cuenta.activa_cta == "S")
    if subcliente_id:
        q = q.filter(Cuenta.subclientes_id_subcli == subcliente_id)
    if estado_id:
        q = q.filter(Cuenta.estados_id_estado == estado_id)
    return q


def minar_resumen(db, subcliente_id=None, estado_id=None) -> dict:
    total, suma, prom, max_ = (
        _cuentas_filtradas(db, subcliente_id, estado_id)
        .with_entities(func.count(Cuenta.id_cta),
                       func.coalesce(func.sum(DEUDA_NUM), 0),
                       func.coalesce(func.avg(DEUDA_NUM), 0),
                       func.coalesce(func.max(DEUDA_NUM), 0))
        .first()
    )
    return {"total": int(total or 0), "deuda_total": float(suma or 0),
            "deuda_promedio": float(prom or 0), "deuda_max": float(max_ or 0)}


def minar_aging(db, subcliente_id=None, estado_id=None) -> list[dict]:
    hoy = date.today()
    out = []
    for nombre, d_min, d_max in _BUCKETS:
        q = _cuentas_filtradas(db, subcliente_id, estado_id).filter(
            Cuenta.fechaingreso_cta <= hoy - timedelta(days=d_min))
        if d_max is not None:
            q = q.filter(Cuenta.fechaingreso_cta > hoy - timedelta(days=d_max + 1))
        cant, deuda = q.with_entities(
            func.count(Cuenta.id_cta), func.coalesce(func.sum(DEUDA_NUM), 0)).first()
        out.append({"bucket": nombre, "cuentas": int(cant or 0), "deuda": float(deuda or 0)})
    return out


def minar_concentracion(db, subcliente_id=None, estado_id=None) -> dict:
    # Calcular total y cantidad en SQL
    total, cant = (_cuentas_filtradas(db, subcliente_id, estado_id)
                   .with_entities(func.coalesce(func.sum(DEUDA_NUM), 0),
                                  func.count(Cuenta.id_cta)).first())
    total = float(total or 0)
    cant = int(cant or 0)

    # Calcular top_n
    top_n = max(1, cant // 10) if cant else 0

    # Calcular deuda_top con subquery
    if top_n > 0:
        sub = (_cuentas_filtradas(db, subcliente_id, estado_id)
               .with_entities(DEUDA_NUM.label("deuda"))
               .order_by(DEUDA_NUM.desc())
               .limit(top_n)
               .subquery())
        deuda_top = db.query(func.coalesce(func.sum(sub.c.deuda), 0)).scalar()
        deuda_top = float(deuda_top or 0)
    else:
        deuda_top = 0.0

    return {"top_cuentas": top_n, "deuda_top": deuda_top,
            "porcentaje": round(deuda_top / total * 100, 1) if total else 0.0}


def minar_gestion(db, desde, hasta, subcliente_id=None, estado_id=None, usuario_id=None) -> dict:
    base = db.query(Contacto).filter(Contacto.activo == "S",
                                     Contacto.fecha_contacto >= desde,
                                     Contacto.fecha_contacto <= hasta)
    if subcliente_id or estado_id:
        base = base.filter(Contacto.cuentas_id_cta.in_(
            _cuentas_filtradas(db, subcliente_id, estado_id).with_entities(Cuenta.id_cta)))
    if usuario_id:
        base = base.filter(Contacto.usuarios_id_usuario == usuario_id)

    contactos = base.count()

    por_accion = [{"desc": d or "—", "cant": int(c)} for d, c in (
        base.outerjoin(Accion, Contacto.acciones_id_accion == Accion.id_accion)
        .with_entities(Accion.desc_accion, func.count()).group_by(Accion.desc_accion)
        .order_by(func.count().desc()).all())]

    filas_res = (base.outerjoin(Resultado, Contacto.resultados_id_resultado == Resultado.id_resultado)
                 .with_entities(Resultado.desc_resultado, func.count())
                 .group_by(Resultado.desc_resultado).order_by(func.count().desc()).all())
    por_resultado = [{"desc": d or "—", "cant": int(c)} for d, c in filas_res]
    compromisos = sum(c for d, c in filas_res if d and "compromiso" in d.lower())
    tasa = round(compromisos / contactos * 100, 1) if contactos else 0.0

    corte = date.today() - timedelta(days=30)
    con_gestion = db.query(Contacto.cuentas_id_cta).filter(
        Contacto.activo == "S", Contacto.fecha_contacto >= corte).distinct()
    q_sin = _cuentas_filtradas(db, subcliente_id, estado_id).filter(
        ~Cuenta.id_cta.in_(con_gestion))
    sin_gestion = q_sin.count()

    # Usuario vive en la DB de auth (otra conexión/base que Cuenta/Contacto):
    # no se puede hacer JOIN contra ella desde esta sesión. Se agrupa por id
    # y el nombre se resuelve aparte, contra auth_db (ver routers/asistente.py).
    top = [{"usuario_id": uid, "cant": int(c)} for uid, c in (
        base.filter(Contacto.usuarios_id_usuario.isnot(None))
        .with_entities(Contacto.usuarios_id_usuario, func.count())
        .group_by(Contacto.usuarios_id_usuario).order_by(func.count().desc()).limit(5).all())]

    return {"contactos": contactos, "por_accion": por_accion, "por_resultado": por_resultado,
            "tasa_compromiso": tasa, "sin_gestion_30d": sin_gestion, "top_gestores": top}


def minar_cobros(db, desde, hasta, deuda_total, subcliente_id=None, estado_id=None) -> dict:
    base = db.query(Cobro).filter(
        Cobro.fcha_cobro >= desde, Cobro.fcha_cobro <= hasta,
        (Cobro.anulado.is_(None)) | (Cobro.anulado != "S"),
    )
    if subcliente_id or estado_id:
        base = base.filter(Cobro.cuentas_id_cta.in_(
            _cuentas_filtradas(db, subcliente_id, estado_id).with_entities(Cuenta.id_cta)))

    mes = func.date_format(Cobro.fcha_cobro, "%Y-%m")
    filas = (base.with_entities(mes, func.coalesce(func.sum(Cobro.importe), 0))
             .group_by(mes).order_by(mes).all())
    por_mes = [{"mes": m, "importe": float(i or 0)} for m, i in filas][-6:]

    tendencia = None
    if len(por_mes) >= 2 and por_mes[-2]["importe"]:
        tendencia = round((por_mes[-1]["importe"] - por_mes[-2]["importe"])
                          / por_mes[-2]["importe"] * 100, 1)

    recuperado = sum(p["importe"] for p in por_mes)
    pct = round(recuperado / deuda_total * 100, 1) if deuda_total else 0.0
    return {"por_mes": por_mes, "tendencia_pct": tendencia,
            "recuperado": recuperado, "pct_recuperado": pct}


def minar_todo(db, desde, hasta, subcliente_id=None, estado_id=None, usuario_id=None) -> dict:
    resumen = minar_resumen(db, subcliente_id, estado_id)
    return {
        "resumen": resumen,
        "aging": minar_aging(db, subcliente_id, estado_id),
        "concentracion": minar_concentracion(db, subcliente_id, estado_id),
        "gestion": minar_gestion(db, desde, hasta, subcliente_id, estado_id, usuario_id),
        "cobros": minar_cobros(db, desde, hasta, resumen["deuda_total"], subcliente_id, estado_id),
    }


_ORDEN_NIVEL = {"critico": 0, "atencion": 1, "info": 2, "positivo": 3}


def _fmt_monto(v: float) -> str:
    return f"$ {v:,.0f}".replace(",", ".")


def generar_hallazgos(datos: dict) -> list[dict]:
    """Evalúa umbrales sobre los datos minados y emite hallazgos con severidad."""
    h: list[dict] = []
    total = datos["resumen"]["total"] or 0
    deuda_total = datos["resumen"]["deuda_total"] or 0.0

    # --- Concentración (Pareto) ---
    conc = datos["concentracion"]
    if conc["porcentaje"] > 70:
        h.append({"nivel": "critico", "titulo": "Concentración extrema de deuda",
                  "detalle": f"El {conc['porcentaje']:.0f}% de la deuda ({_fmt_monto(conc['deuda_top'])}) "
                             f"está en solo {conc['top_cuentas']} cuentas (top 10%). "
                             "Priorizar gestión personalizada sobre ese núcleo."})
    elif conc["porcentaje"] > 50:
        h.append({"nivel": "atencion", "titulo": "Concentración alta de deuda",
                  "detalle": f"El {conc['porcentaje']:.0f}% de la deuda se concentra en "
                             f"{conc['top_cuentas']} cuentas. Un puñado de acuerdos mueve la aguja."})

    # --- Aging ---
    bucket_viejo = next((b for b in datos["aging"] if b["bucket"] == "+180"), None)
    if bucket_viejo and deuda_total:
        pct_viejo = bucket_viejo["deuda"] / deuda_total * 100
        if pct_viejo > 40:
            h.append({"nivel": "atencion", "titulo": "Cartera con antigüedad pesada",
                      "detalle": f"El {pct_viejo:.0f}% de la deuda ({_fmt_monto(bucket_viejo['deuda'])}, "
                                 f"{bucket_viejo['cuentas']} cuentas) tiene más de 180 días. "
                                 "La recuperabilidad cae con la antigüedad: evaluar vía judicial o quitas."})

    # --- Gestión ---
    g = datos["gestion"]
    if total:
        pct_sin = g["sin_gestion_30d"] / total * 100
        if pct_sin > 20:
            h.append({"nivel": "critico", "titulo": "Cuentas sin gestión reciente",
                      "detalle": f"{g['sin_gestion_30d']} cuentas ({pct_sin:.0f}% de la cartera) no tienen "
                                 "gestión hace más de 30 días. Deuda fría es deuda perdida: reasignar."})
        elif pct_sin > 10:
            h.append({"nivel": "atencion", "titulo": "Cuentas sin gestión reciente",
                      "detalle": f"{g['sin_gestion_30d']} cuentas ({pct_sin:.0f}%) sin contacto hace más "
                                 "de 30 días. Programar barrido de re-contacto."})
    if g["tasa_compromiso"] > 30:
        h.append({"nivel": "positivo", "titulo": "Buena tasa de compromiso",
                  "detalle": f"El {g['tasa_compromiso']:.0f}% de los contactos del período terminó en "
                             "compromiso de pago. La estrategia de contacto está funcionando."})

    # --- Cobros ---
    c = datos["cobros"]
    if c["tendencia_pct"] is not None:
        if c["tendencia_pct"] < -15:
            h.append({"nivel": "critico", "titulo": "Recaudación en caída",
                      "detalle": f"La recaudación cayó {abs(c['tendencia_pct']):.0f}% contra el mes "
                                 f"anterior. Recuperado del período: {_fmt_monto(c['recuperado'])}. "
                                 "Revisar convenios vigentes y promesas incumplidas."})
        elif c["tendencia_pct"] > 15:
            h.append({"nivel": "positivo", "titulo": "Recaudación en alza",
                      "detalle": f"La recaudación subió {c['tendencia_pct']:.0f}% contra el mes anterior "
                                 f"({_fmt_monto(c['recuperado'])} recuperados en el período)."})
    if deuda_total and c["pct_recuperado"] < 5 and c["recuperado"] >= 0:
        h.append({"nivel": "atencion", "titulo": "Recupero bajo sobre deuda",
                  "detalle": f"Lo cobrado en el período ({_fmt_monto(c['recuperado'])}) representa solo el "
                             f"{c['pct_recuperado']:.1f}% de la deuda del subconjunto analizado."})

    # --- Sin actividad ---
    if g["contactos"] == 0 and not c["por_mes"]:
        h.append({"nivel": "info", "titulo": "Sin actividad en el período",
                  "detalle": "No hay contactos ni cobros registrados con los filtros aplicados. "
                             "Ampliar el período o revisar los filtros."})

    h.sort(key=lambda x: _ORDEN_NIVEL[x["nivel"]])
    return h


def generar_narrativa(datos: dict, hallazgos: list[dict], filtros: dict) -> str:
    """Párrafo ejecutivo: alcance, estado dominante y acción recomendada."""
    r = datos["resumen"]
    partes = [f"{filtros['alcance']}, {filtros['periodo']}: {r['total']} cuentas por "
              f"{_fmt_monto(r['deuda_total'])} de deuda "
              f"(promedio {_fmt_monto(r['deuda_promedio'])})."]

    c = datos["cobros"]
    if c["recuperado"]:
        partes.append(f"Se recuperaron {_fmt_monto(c['recuperado'])} "
                      f"({c['pct_recuperado']:.1f}% de la deuda analizada).")

    if hallazgos:
        dominante = hallazgos[0]
        if dominante["nivel"] == "critico":
            partes.append(f"Foco inmediato: {dominante['titulo'].lower()} — {dominante['detalle']}")
        elif dominante["nivel"] == "atencion":
            partes.append(f"Punto a vigilar: {dominante['titulo'].lower()}.")
        else:
            partes.append("La cartera no presenta alertas relevantes con los filtros aplicados.")
    else:
        partes.append("La cartera no presenta alertas relevantes con los filtros aplicados.")

    return " ".join(partes)
