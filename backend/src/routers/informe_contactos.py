from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.auth_database import get_auth_db
from src.core.security import get_current_user
from src.core.export import to_excel_response
from src.models.contactos import Contacto
from src.models.cuentas import Cuenta, Entidad
from src.models.catalogos import Accion, Resultado, SubEstado
from src.models.usuario import Usuario

router = APIRouter(prefix="/informes/contactos", tags=["Informes"])

COLUMNS = [
    ("id_cta", "Cuenta"),
    ("subestado", "Subestado"),
    ("matricula", "Matrícula"),
    ("razon_social", "Razón social"),
    ("fecha", "Fecha"),
    ("hora", "Hora"),
    ("nota", "Nota"),
    ("accion", "Acción"),
    ("resultado", "Resultado"),
    ("usuario", "Usuario"),
]


def _consultar(db, db_auth, desde, hasta, accion_id, resultado_id, usuario_id, subestado_id=None):
    # La tabla usuarios vive en la DB de autenticación, no en la de gestión:
    # se resuelve aparte con la sesión de auth para no romper el join principal.
    q = (
        db.query(
            Contacto,
            Cuenta.entidades_matricula_ent,
            Entidad.razon_social_ent,
            Accion.desc_accion,
            Resultado.desc_resultado,
            SubEstado.desc_sub_est,
        )
        .join(Cuenta, Contacto.cuentas_id_cta == Cuenta.id_cta)
        .join(Entidad, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
        .outerjoin(SubEstado, Cuenta.sub_estados_id_sub_est == SubEstado.id_sub_est)
        .outerjoin(Accion, Contacto.acciones_id_accion == Accion.id_accion)
        .outerjoin(Resultado, Contacto.resultados_id_resultado == Resultado.id_resultado)
        .filter(Contacto.activo == "S")
    )
    if desde:
        q = q.filter(Contacto.fecha_contacto >= desde)
    if hasta:
        q = q.filter(Contacto.fecha_contacto <= hasta)
    if accion_id:
        q = q.filter(Contacto.acciones_id_accion == accion_id)
    if resultado_id:
        q = q.filter(Contacto.resultados_id_resultado == resultado_id)
    if usuario_id:
        q = q.filter(Contacto.usuarios_id_usuario == usuario_id)
    if subestado_id:
        q = q.filter(Cuenta.sub_estados_id_sub_est == subestado_id)
    filas = []
    for contacto, matricula, razon, desc_accion, desc_resultado, subestado in q.order_by(Contacto.fecha_contacto.desc()).all():
        filas.append({
            "id_cta": contacto.cuentas_id_cta,
            "subestado": subestado,
            "matricula": matricula,
            "razon_social": razon,
            "fecha": contacto.fecha_contacto.isoformat() if contacto.fecha_contacto else None,
            "hora": contacto.hora_contacto,
            "nota": contacto.nota_contacto.decode() if contacto.nota_contacto else None,
            "accion": desc_accion,
            "resultado": desc_resultado,
            "usuario_id": contacto.usuarios_id_usuario,
        })

    # Resolver nombres de usuario desde la DB de auth en una sola consulta
    ids = {f["usuario_id"] for f in filas if f["usuario_id"] is not None}
    nombres = {}
    if ids:
        for u in db_auth.query(Usuario).filter(Usuario.id_usuario.in_(ids)).all():
            nombres[u.id_usuario] = u.loguin_usuario
    for f in filas:
        f["usuario"] = nombres.get(f.pop("usuario_id"))

    return filas


@router.get("")
def informe_contactos(
    desde: Optional[date] = Query(None),
    hasta: Optional[date] = Query(None),
    accion_id: Optional[int] = Query(None),
    resultado_id: Optional[int] = Query(None),
    usuario_id: Optional[int] = Query(None),
    subestado_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    db_auth: Session = Depends(get_auth_db),
    _user: dict = Depends(get_current_user),
):
    filas = _consultar(db, db_auth, desde, hasta, accion_id, resultado_id, usuario_id, subestado_id)
    return {"filas": filas}


@router.get("/export")
def exportar_contactos(
    desde: Optional[date] = Query(None),
    hasta: Optional[date] = Query(None),
    accion_id: Optional[int] = Query(None),
    resultado_id: Optional[int] = Query(None),
    usuario_id: Optional[int] = Query(None),
    subestado_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    db_auth: Session = Depends(get_auth_db),
    _user: dict = Depends(get_current_user),
):
    filas = _consultar(db, db_auth, desde, hasta, accion_id, resultado_id, usuario_id, subestado_id)
    return to_excel_response(filas, COLUMNS, "informe_contactos.xlsx")
