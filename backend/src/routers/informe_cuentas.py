from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.export import to_excel_response
from src.models.cuentas import Cuenta, Entidad
from src.models.contactos import Contacto
from src.models.catalogos import Accion, Resultado
from src.models.financiero import Cobro

router = APIRouter(prefix="/informes/cuentas", tags=["Informes"])

COLUMNS = [
    ("id_cta", "Cuenta"),
    ("nombre", "Nombre"),
    ("matricula", "Matricula"),
    ("fecha_ingreso", "Fecha Ingreso"),
    ("fecha_ultimo_contacto", "Fecha Ult. Contacto"),
    ("ultimo_contacto", "Ultimo Contacto"),
    ("fecha_ultimo_cobro", "Fecha Ult. Cobro"),
    ("monto", "Monto"),
]


def _ultimo_contacto_por_cuenta(db: Session) -> dict:
    """Fecha + descripción (resultado/acción + nota) del último contacto activo
    de cada cuenta."""
    sub = (
        db.query(Contacto.cuentas_id_cta.label("id_cta"), func.max(Contacto.fecha_contacto).label("ultima_fecha"))
        .filter(Contacto.activo == "S")
        .group_by(Contacto.cuentas_id_cta)
        .subquery()
    )
    filas = (
        db.query(Contacto.cuentas_id_cta, Contacto.fecha_contacto, Contacto.nota_contacto,
                  Resultado.desc_resultado, Accion.desc_accion)
        .join(sub, (Contacto.cuentas_id_cta == sub.c.id_cta) & (Contacto.fecha_contacto == sub.c.ultima_fecha))
        .outerjoin(Resultado, Contacto.resultados_id_resultado == Resultado.id_resultado)
        .outerjoin(Accion, Contacto.acciones_id_accion == Accion.id_accion)
        .filter(Contacto.activo == "S")
        .all()
    )
    out = {}
    for id_cta, fecha, nota_contacto, desc_resultado, desc_accion in filas:
        desc = desc_resultado or desc_accion
        nota = nota_contacto.decode() if nota_contacto else None
        if desc and nota:
            texto = f"{desc} — {nota}"
        else:
            texto = desc or nota
        out[id_cta] = (fecha, texto)
    return out


def _ultimo_cobro_por_cuenta(db: Session) -> dict:
    """Fecha + importe del último cobro vigente (no anulado) de cada cuenta."""
    sub = (
        db.query(Cobro.cuentas_id_cta.label("id_cta"), func.max(Cobro.fcha_cobro).label("ultima_fecha"))
        .filter((Cobro.anulado.is_(None)) | (Cobro.anulado != "S"))
        .group_by(Cobro.cuentas_id_cta)
        .subquery()
    )
    filas = (
        db.query(Cobro.cuentas_id_cta, Cobro.fcha_cobro, Cobro.importe)
        .join(sub, (Cobro.cuentas_id_cta == sub.c.id_cta) & (Cobro.fcha_cobro == sub.c.ultima_fecha))
        .filter((Cobro.anulado.is_(None)) | (Cobro.anulado != "S"))
        .all()
    )
    out = {}
    for id_cta, fecha, importe in filas:
        out[id_cta] = (fecha, importe)
    return out


def _consultar(db: Session, subestado_id: Optional[int] = None):
    query = (
        db.query(Cuenta, Entidad.razon_social_ent)
        .outerjoin(Entidad, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
    )
    if subestado_id:
        query = query.filter(Cuenta.sub_estados_id_sub_est == subestado_id)

    cuentas = query.order_by(Cuenta.id_cta.desc()).all()
    ultimo_contacto = _ultimo_contacto_por_cuenta(db)
    ultimo_cobro = _ultimo_cobro_por_cuenta(db)

    filas = []
    for cuenta, razon in cuentas:
        fecha_contacto, desc_contacto = ultimo_contacto.get(cuenta.id_cta, (None, None))
        fecha_cobro, importe_cobro = ultimo_cobro.get(cuenta.id_cta, (None, None))
        filas.append(
            {
                "id_cta": cuenta.id_cta,
                "nombre": razon,
                "matricula": cuenta.entidades_matricula_ent,
                "fecha_ingreso": cuenta.fechaingreso_cta.isoformat() if cuenta.fechaingreso_cta else None,
                "fecha_ultimo_contacto": fecha_contacto.isoformat() if fecha_contacto else None,
                "ultimo_contacto": desc_contacto,
                "fecha_ultimo_cobro": fecha_cobro.isoformat() if fecha_cobro else None,
                "monto": str(importe_cobro) if importe_cobro is not None else None,
            }
        )
    return filas


@router.get("")
def informe_cuentas(
    subestado_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return {"filas": _consultar(db, subestado_id)}


@router.get("/export")
def exportar_cuentas(
    subestado_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return to_excel_response(_consultar(db, subestado_id), COLUMNS, "informe_cuentas.xlsx")
