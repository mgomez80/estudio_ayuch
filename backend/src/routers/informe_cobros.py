from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.export import to_excel_response
from src.models.cuentas import Cuenta, Entidad
from src.models.catalogos import Concepto
from src.models.financiero import Cobro
from src.routers.cobros_abm import CONCEPTO_PAGO_A_CUENTA

router = APIRouter(prefix="/informes/cobros", tags=["Informes"])

COLUMNS = [
    ("id_cobros", "Cobro"),
    ("fecha", "Fecha"),
    ("id_cta", "Cuenta"),
    ("matricula", "Matrícula"),
    ("razon_social", "Cuenta (nombre)"),
    ("concepto", "Concepto"),
    ("importe", "Importe"),
    ("rendido", "Rendido"),
    ("anulado", "Anulado"),
]


def _consultar(
    db: Session,
    desde: Optional[date] = None,
    hasta: Optional[date] = None,
    rendido: Optional[str] = None,
    incluir_anulados: bool = False,
):
    query = (
        db.query(Cobro, Cuenta.entidades_matricula_ent, Entidad.razon_social_ent, Concepto.desc_concepto)
        .join(Cuenta, Cobro.cuentas_id_cta == Cuenta.id_cta)
        .outerjoin(Entidad, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
        .outerjoin(Concepto, Cobro.conceptos_id_concepto == Concepto.id_concepto)
    )
    if not incluir_anulados:
        query = query.filter((Cobro.anulado.is_(None)) | (Cobro.anulado != "S"))
    if desde:
        query = query.filter(Cobro.fcha_cobro >= desde)
    if hasta:
        query = query.filter(Cobro.fcha_cobro <= hasta)
    if rendido in ("S", "N"):
        query = query.filter(Cobro.rendido == rendido)

    filas = []
    for cobro, matricula, razon_social, concepto_desc in query.order_by(Cobro.fcha_cobro.desc()).all():
        filas.append(
            {
                "id_cobros": cobro.id_cobros,
                "fecha": cobro.fcha_cobro.isoformat() if cobro.fcha_cobro else None,
                "id_cta": cobro.cuentas_id_cta,
                "matricula": matricula,
                "razon_social": razon_social,
                "concepto": concepto_desc or CONCEPTO_PAGO_A_CUENTA,
                "importe": str(cobro.importe) if cobro.importe is not None else None,
                "rendido": cobro.rendido,
                "anulado": cobro.anulado,
            }
        )
    return filas


@router.get("")
def informe_cobros(
    desde: Optional[date] = Query(None),
    hasta: Optional[date] = Query(None),
    rendido: Optional[str] = Query(None, description="S=rendido, N=pendiente, omitir para todos"),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return {"filas": _consultar(db, desde, hasta, rendido)}


@router.get("/export")
def exportar_cobros(
    desde: Optional[date] = Query(None),
    hasta: Optional[date] = Query(None),
    rendido: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    return to_excel_response(_consultar(db, desde, hasta, rendido), COLUMNS, "informe_cobros.xlsx")
