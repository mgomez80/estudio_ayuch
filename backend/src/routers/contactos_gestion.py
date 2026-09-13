from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.contactos import Contacto

router = APIRouter(prefix="", tags=["Contactos"])


# ============================================================================
# Schemas Pydantic
# ============================================================================

class ContactoGestionIn(BaseModel):
    """Schema para crear un contacto de gestión."""
    fecha_contacto: date
    hora_contacto: str
    nota: Optional[str] = None


class ContactoUpdateIn(BaseModel):
    """Schema para actualizar un contacto de gestión."""
    fecha_contacto: Optional[date] = None
    hora_contacto: Optional[str] = None
    nota: Optional[str] = None


class ContactoGestionOut(BaseModel):
    """Schema de salida para contacto de gestión."""
    model_config = ConfigDict(from_attributes=True)

    id_contacto: int
    cuentas_id_cta: int
    fecha_contacto: Optional[date] = None
    hora_contacto: Optional[str] = None
    nota: Optional[str] = None
    activo: Optional[str] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/cuentas/{id_cta}/contactos", response_model=ContactoGestionOut, status_code=201)
def crear_contacto(
    id_cta: int,
    payload: ContactoGestionIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """
    Crear un nuevo registro de gestión (contacto) para una cuenta.
    Requiere autenticación (usuario extraído del JWT).
    """
    # Crear el contacto
    nota_bytes = payload.nota.encode() if payload.nota else None

    nuevo_contacto = Contacto(
        usuarios_id_usuario=_user["id_usuario"],
        cuentas_id_cta=id_cta,
        fecha_contacto=payload.fecha_contacto,
        hora_contacto=payload.hora_contacto,
        nota_contacto=nota_bytes,
        activo="S",
    )

    db.add(nuevo_contacto)
    db.commit()
    db.refresh(nuevo_contacto)

    # Construir la respuesta decodificando nota
    respuesta = ContactoGestionOut.model_validate(nuevo_contacto)
    respuesta.nota = nuevo_contacto.nota_contacto.decode() if nuevo_contacto.nota_contacto else None

    return respuesta


@router.patch("/contactos/{id_contacto}", response_model=ContactoGestionOut)
def editar_contacto(
    id_contacto: int,
    payload: ContactoUpdateIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """
    Editar un contacto de gestión existente.
    Solo se actualizan los campos presentes en el payload.
    """
    contacto = db.query(Contacto).filter(Contacto.id_contacto == id_contacto).first()
    if not contacto:
        raise HTTPException(status_code=404, detail=f"Contacto {id_contacto} no encontrado")

    if payload.fecha_contacto is not None:
        contacto.fecha_contacto = payload.fecha_contacto

    if payload.hora_contacto is not None:
        contacto.hora_contacto = payload.hora_contacto

    if payload.nota is not None:
        contacto.nota_contacto = payload.nota.encode() if payload.nota else None

    db.commit()
    db.refresh(contacto)

    # Construir la respuesta decodificando nota
    respuesta = ContactoGestionOut.model_validate(contacto)
    respuesta.nota = contacto.nota_contacto.decode() if contacto.nota_contacto else None

    return respuesta


@router.patch("/contactos/{id_contacto}/baja")
def dar_baja_contacto(
    id_contacto: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Marcar un contacto como inactivo (baja lógica)."""
    contacto = db.query(Contacto).filter(Contacto.id_contacto == id_contacto).first()
    if not contacto:
        raise HTTPException(status_code=404, detail=f"Contacto {id_contacto} no encontrado")

    contacto.activo = "N"
    db.commit()

    return {"message": f"Contacto {id_contacto} dado de baja"}


@router.get("/catalogos/subclientes")
def listar_subclientes(db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    from src.models.cuentas import Subcliente
    filas = (db.query(Subcliente).filter(Subcliente.activo_subcli == "S")
             .order_by(Subcliente.nombre_subcli).all())
    return [{"id_subcli": s.id_subcli, "nombre_subcli": s.nombre_subcli} for s in filas]


@router.get("/catalogos/clientes")
def listar_clientes(db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    from src.models.cuentas import Cliente
    filas = db.query(Cliente).order_by(Cliente.desc_cliente).all()
    return [{"id_cliente": c.id_cliente, "cuenta_cliente": c.cuenta_cliente, "desc_cliente": c.desc_cliente} for c in filas]


@router.get("/catalogos/estados")
def listar_estados(db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    from src.models.catalogos import Estado
    filas = db.query(Estado).filter(Estado.activo == "S").order_by(Estado.desc_estado).all()
    return [{"id_estado": e.id_estado, "desc_estado": e.desc_estado} for e in filas]
