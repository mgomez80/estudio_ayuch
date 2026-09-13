import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.auth_database import get_auth_db
from src.core.security import get_current_admin
from src.models.usuario import Usuario

router = APIRouter(prefix="/config", tags=["Configuración"])


class UsuarioCreate(BaseModel):
    loguin_usuario: str
    password: str
    nombre_completo: str
    rol: str
    perfiles_id_perfil: int | None = None


class UsuarioUpdate(BaseModel):
    password: str | None = None
    nombre_completo: str | None = None
    rol: str | None = None
    perfiles_id_perfil: int | None = None
    activo: bool | None = None


class UsuarioOut(BaseModel):
    id_usuario: int
    loguin_usuario: str
    nombre_completo: str | None
    rol: str
    activo: bool
    perfiles_id_perfil: int | None

    class Config:
        from_attributes = True


def hash_password(plain_password: str) -> str:
    """Hash password using bcrypt, same as verify_password expects."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode(), salt).decode()


@router.get("/usuarios", response_model=list[UsuarioOut])
def list_usuarios(
    db: Session = Depends(get_auth_db),
    _admin: dict = Depends(get_current_admin),
):
    """Lista todos los usuarios."""
    usuarios = db.query(Usuario).all()
    return usuarios


@router.get("/usuarios/{id_usuario}", response_model=UsuarioOut)
def get_usuario(
    id_usuario: int,
    db: Session = Depends(get_auth_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtiene un usuario por ID."""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@router.post("/usuarios", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(
    payload: UsuarioCreate,
    db: Session = Depends(get_auth_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crea un nuevo usuario."""
    # Validar que el login no exista
    existing = db.query(Usuario).filter(Usuario.loguin_usuario == payload.loguin_usuario).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")

    # Hash password
    password_hash = hash_password(payload.password)

    # Crear usuario
    nuevo_usuario = Usuario(
        loguin_usuario=payload.loguin_usuario,
        password_hash=password_hash,
        nombre_completo=payload.nombre_completo,
        rol=payload.rol,
        perfiles_id_perfil=payload.perfiles_id_perfil,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.patch("/usuarios/{id_usuario}", response_model=UsuarioOut)
def update_usuario(
    id_usuario: int,
    payload: UsuarioUpdate,
    db: Session = Depends(get_auth_db),
    _admin: dict = Depends(get_current_admin),
):
    """Edita un usuario."""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Actualizar campos
    if payload.password is not None:
        usuario.password_hash = hash_password(payload.password)
    if payload.nombre_completo is not None:
        usuario.nombre_completo = payload.nombre_completo
    if payload.rol is not None:
        usuario.rol = payload.rol
    if payload.perfiles_id_perfil is not None:
        usuario.perfiles_id_perfil = payload.perfiles_id_perfil
    if payload.activo is not None:
        usuario.activo = payload.activo

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    id_usuario: int,
    db: Session = Depends(get_auth_db),
    _admin: dict = Depends(get_current_admin),
):
    """Soft-delete de un usuario (activo=False)."""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    usuario.activo = False
    db.commit()
