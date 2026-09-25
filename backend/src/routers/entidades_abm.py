"""
ABM de teléfonos, direcciones y mails de una entidad (deudor), identificada
por su matrícula. El frontend (TelefonosDomicilios.tsx) ya llamaba a estos
endpoints -- /entidades/{matricula}/telefonos|direcciones|mails -- pero el
router nunca se había creado, así que toda la sección tiraba 404.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.cuentas import Entidad
from src.models.contactos import Telefono, Direccion, Mail

router = APIRouter(prefix="/entidades/{matricula}", tags=["Teléfonos y Domicilios"])


def _get_entidad_o_404(db: Session, matricula: str) -> Entidad:
    entidad = db.query(Entidad).filter(Entidad.matricula_ent == matricula).first()
    if not entidad:
        raise HTTPException(status_code=404, detail=f"Entidad {matricula} no encontrada")
    return entidad


# ============================================================================
# TELÉFONOS
# ============================================================================

class TelefonoIn(BaseModel):
    tipo_tel: str
    codigo_area_tel: str
    numero_tel: str
    observaciones_tel: Optional[str] = None


class TelefonoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_tel: int
    tipo_tel: Optional[str] = None
    codigo_area_tel: Optional[str] = None
    numero_tel: Optional[str] = None
    observaciones_tel: Optional[str] = None
    activo_tel: Optional[str] = None


@router.get("/telefonos", response_model=list[TelefonoOut])
def listar_telefonos(matricula: str, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    return (
        db.query(Telefono)
        .filter(Telefono.entidades_matricula_ent == matricula)
        .order_by(Telefono.id_tel.desc())
        .all()
    )


@router.post("/telefonos", response_model=TelefonoOut, status_code=status.HTTP_201_CREATED)
def crear_telefono(matricula: str, payload: TelefonoIn, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    _get_entidad_o_404(db, matricula)
    nuevo = Telefono(entidades_matricula_ent=matricula, activo_tel="S", **payload.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/telefonos/{id_tel}", response_model=TelefonoOut)
def editar_telefono(matricula: str, id_tel: int, payload: TelefonoIn, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    tel = db.query(Telefono).filter(Telefono.id_tel == id_tel, Telefono.entidades_matricula_ent == matricula).first()
    if not tel:
        raise HTTPException(status_code=404, detail="Teléfono no encontrado")
    for k, v in payload.model_dump().items():
        setattr(tel, k, v)
    db.commit()
    db.refresh(tel)
    return tel


@router.patch("/telefonos/{id_tel}/baja")
def baja_telefono(matricula: str, id_tel: int, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    tel = db.query(Telefono).filter(Telefono.id_tel == id_tel, Telefono.entidades_matricula_ent == matricula).first()
    if not tel:
        raise HTTPException(status_code=404, detail="Teléfono no encontrado")
    tel.activo_tel = "N"
    db.commit()
    return {"message": "Teléfono dado de baja"}


@router.patch("/telefonos/{id_tel}/reactivar")
def reactivar_telefono(matricula: str, id_tel: int, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    tel = db.query(Telefono).filter(Telefono.id_tel == id_tel, Telefono.entidades_matricula_ent == matricula).first()
    if not tel:
        raise HTTPException(status_code=404, detail="Teléfono no encontrado")
    tel.activo_tel = "S"
    db.commit()
    return {"message": "Teléfono reactivado"}


# ============================================================================
# DIRECCIONES
# ============================================================================

class DireccionIn(BaseModel):
    calle_dir: str
    nro_dir: str
    piso_dir: Optional[str] = None
    dpto_dir: Optional[str] = None
    barrio_dir: str
    cp_dir: str
    localidad_dir: str
    departamento_dir: Optional[str] = None
    provincia_dir: str
    tipo_dir: str
    observacion_dir: Optional[str] = None


class DireccionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_dir: int
    calle_dir: Optional[str] = None
    nro_dir: Optional[str] = None
    piso_dir: Optional[str] = None
    dpto_dir: Optional[str] = None
    barrio_dir: Optional[str] = None
    cp_dir: Optional[str] = None
    localidad_dir: Optional[str] = None
    departamento_dir: Optional[str] = None
    provincia_dir: Optional[str] = None
    tipo_dir: Optional[str] = None
    observacion_dir: Optional[str] = None
    activa_dir: Optional[str] = None


@router.get("/direcciones", response_model=list[DireccionOut])
def listar_direcciones(matricula: str, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    return (
        db.query(Direccion)
        .filter(Direccion.entidades_matricula_ent == matricula)
        .order_by(Direccion.id_dir.desc())
        .all()
    )


@router.post("/direcciones", response_model=DireccionOut, status_code=status.HTTP_201_CREATED)
def crear_direccion(matricula: str, payload: DireccionIn, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    _get_entidad_o_404(db, matricula)
    nueva = Direccion(entidades_matricula_ent=matricula, activa_dir="S", **payload.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.patch("/direcciones/{id_dir}", response_model=DireccionOut)
def editar_direccion(matricula: str, id_dir: int, payload: DireccionIn, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    dir_ = db.query(Direccion).filter(Direccion.id_dir == id_dir, Direccion.entidades_matricula_ent == matricula).first()
    if not dir_:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    for k, v in payload.model_dump().items():
        setattr(dir_, k, v)
    db.commit()
    db.refresh(dir_)
    return dir_


@router.patch("/direcciones/{id_dir}/baja")
def baja_direccion(matricula: str, id_dir: int, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    dir_ = db.query(Direccion).filter(Direccion.id_dir == id_dir, Direccion.entidades_matricula_ent == matricula).first()
    if not dir_:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    dir_.activa_dir = "N"
    db.commit()
    return {"message": "Domicilio dado de baja"}


@router.patch("/direcciones/{id_dir}/reactivar")
def reactivar_direccion(matricula: str, id_dir: int, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    dir_ = db.query(Direccion).filter(Direccion.id_dir == id_dir, Direccion.entidades_matricula_ent == matricula).first()
    if not dir_:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    dir_.activa_dir = "S"
    db.commit()
    return {"message": "Domicilio reactivado"}


# ============================================================================
# MAILS
# ============================================================================

class MailIn(BaseModel):
    mail: str
    tipo_mail: str


class MailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_mails: int
    mail: Optional[str] = None
    tipo_mail: Optional[str] = None
    activo_mail: Optional[str] = None


@router.get("/mails", response_model=list[MailOut])
def listar_mails(matricula: str, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    return (
        db.query(Mail)
        .filter(Mail.entidades_matricula_ent == matricula)
        .order_by(Mail.id_mails.desc())
        .all()
    )


@router.post("/mails", response_model=MailOut, status_code=status.HTTP_201_CREATED)
def crear_mail(matricula: str, payload: MailIn, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    _get_entidad_o_404(db, matricula)
    nuevo = Mail(entidades_matricula_ent=matricula, activo_mail="S", **payload.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/mails/{id_mails}", response_model=MailOut)
def editar_mail(matricula: str, id_mails: int, payload: MailIn, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    mail = db.query(Mail).filter(Mail.id_mails == id_mails, Mail.entidades_matricula_ent == matricula).first()
    if not mail:
        raise HTTPException(status_code=404, detail="Mail no encontrado")
    for k, v in payload.model_dump().items():
        setattr(mail, k, v)
    db.commit()
    db.refresh(mail)
    return mail


@router.patch("/mails/{id_mails}/baja")
def baja_mail(matricula: str, id_mails: int, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    mail = db.query(Mail).filter(Mail.id_mails == id_mails, Mail.entidades_matricula_ent == matricula).first()
    if not mail:
        raise HTTPException(status_code=404, detail="Mail no encontrado")
    mail.activo_mail = "N"
    db.commit()
    return {"message": "Mail dado de baja"}


@router.patch("/mails/{id_mails}/reactivar")
def reactivar_mail(matricula: str, id_mails: int, db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    mail = db.query(Mail).filter(Mail.id_mails == id_mails, Mail.entidades_matricula_ent == matricula).first()
    if not mail:
        raise HTTPException(status_code=404, detail="Mail no encontrado")
    mail.activo_mail = "S"
    db.commit()
    return {"message": "Mail reactivado"}
