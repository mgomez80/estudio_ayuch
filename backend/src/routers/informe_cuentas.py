from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.export import to_excel_response
from src.models.cuentas import Cuenta, Entidad, Cliente, Subcliente
from src.models.catalogos import Estado, SubEstado

router = APIRouter(prefix="/informes/cuentas", tags=["Informes"])

COLUMNS = [
    ("id_cta", "Cuenta"),
    ("subestado", "Subestado"),
    ("estado", "Estado"),
    ("matricula", "Matrícula"),
    ("razon_social", "Razón social"),
    ("cuenta_cliente", "Cuenta cliente"),
    ("cliente", "Cliente"),
    ("subcliente", "Subcliente"),
    ("deuda_actual", "Deuda actual"),
    ("deuda_transferida", "Deuda transferida"),
    ("fecha_ingreso", "Fecha de ingreso"),
    ("empleador", "Empleador"),
    ("judicial", "Judicial"),
    ("activa", "Activa"),
    ("observacion", "Observación"),
]


def _consultar(db: Session, subestado_id: Optional[int] = None):
    query = (
        db.query(
            Cuenta,
            Entidad.razon_social_ent,
            SubEstado.desc_sub_est,
            Estado.desc_estado,
            Cliente.desc_cliente,
            Subcliente.nombre_subcli,
        )
        .outerjoin(Entidad, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
        .outerjoin(SubEstado, Cuenta.sub_estados_id_sub_est == SubEstado.id_sub_est)
        .outerjoin(Estado, Cuenta.estados_id_estado == Estado.id_estado)
        .outerjoin(Subcliente, Cuenta.subclientes_id_subcli == Subcliente.id_subcli)
        .outerjoin(
            Cliente,
            (Subcliente.clientes_id_cliente == Cliente.id_cliente)
            & (Subcliente.clientes_cuenta_cliente == Cliente.cuenta_cliente),
        )
    )
    if subestado_id:
        query = query.filter(Cuenta.sub_estados_id_sub_est == subestado_id)

    filas = []
    for cuenta, razon, subestado, estado, cliente, subcliente in query.order_by(Cuenta.id_cta.desc()).all():
        filas.append(
            {
                "id_cta": cuenta.id_cta,
                "subestado": subestado,
                "estado": estado,
                "matricula": cuenta.entidades_matricula_ent,
                "razon_social": razon,
                "cuenta_cliente": cuenta.cuenta_cliente,
                "cliente": cliente,
                "subcliente": subcliente,
                "deuda_actual": str(cuenta.deudaact_cta) if cuenta.deudaact_cta is not None else None,
                "deuda_transferida": str(cuenta.deudatrans_cta) if cuenta.deudatrans_cta is not None else None,
                "fecha_ingreso": cuenta.fechaingreso_cta.isoformat() if cuenta.fechaingreso_cta else None,
                "empleador": cuenta.empleador_cta,
                "judicial": cuenta.judicial,
                "activa": cuenta.activa_cta,
                "observacion": cuenta.observacion_cta,
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