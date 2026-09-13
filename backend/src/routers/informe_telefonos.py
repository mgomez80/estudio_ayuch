from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.core.export import to_excel_response
from src.models.contactos import Telefono
from src.models.cuentas import Entidad, Cuenta, Subcliente, Cliente

router = APIRouter(prefix="/informes/telefonos", tags=["Informes"])

COLUMNS = [
    ("id_cta", "Cuenta"),
    ("cliente", "Cliente"),
    ("subcliente", "Subcliente"),
    ("razon_social", "Razón social"),
    ("tipo", "Tipo"),
    ("cod_area", "Código área"),
    ("numero", "Número"),
    ("activo", "Activo"),
]


def _consultar(db, activo, tipo, cliente_id=None, subcliente_id=None):
    q = (
        db.query(Telefono, Entidad.razon_social_ent, Cuenta.id_cta, Subcliente.nombre_subcli, Cliente.desc_cliente)
        .join(Entidad, Telefono.entidades_matricula_ent == Entidad.matricula_ent)
        .join(Cuenta, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
        .outerjoin(Subcliente, Cuenta.subclientes_id_subcli == Subcliente.id_subcli)
        .outerjoin(Cliente, (Subcliente.clientes_id_cliente == Cliente.id_cliente) & (Subcliente.clientes_cuenta_cliente == Cliente.cuenta_cliente))
    )
    if activo:
        q = q.filter(Telefono.activo_tel == activo)
    if tipo:
        q = q.filter(Telefono.tipo_tel == tipo)
    if cliente_id:
        q = q.filter(Cliente.id_cliente == cliente_id)
    if subcliente_id:
        q = q.filter(Subcliente.id_subcli == subcliente_id)
    filas = []
    for telefono, razon, id_cta, subcli, cliente in q.order_by(Entidad.razon_social_ent).all():
        filas.append({
            "id_cta": id_cta,
            "cliente": cliente,
            "subcliente": subcli,
            "razon_social": razon,
            "tipo": telefono.tipo_tel,
            "cod_area": telefono.codigo_area_tel,
            "numero": telefono.numero_tel,
            "activo": telefono.activo_tel,
        })
    return filas


@router.get("/tipos")
def listar_tipos(db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    tipos = db.query(Telefono.tipo_tel).distinct().all()
    return [t[0] for t in tipos if t[0]]

@router.get("")
def informe_telefonos(
    activo: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    cliente_id: Optional[int] = Query(None),
    subcliente_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    filas = _consultar(db, activo, tipo, cliente_id, subcliente_id)
    return {"filas": filas}


@router.get("/export")
def exportar_telefonos(
    activo: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    cliente_id: Optional[int] = Query(None),
    subcliente_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    filas = _consultar(db, activo, tipo, cliente_id, subcliente_id)
    return to_excel_response(filas, COLUMNS, "informe_telefonos.xlsx")
