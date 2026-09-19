from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.core.auth_database import get_auth_db
from src.core.security import verify_password, create_access_token
from src.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Hash dummy usado para mantener tiempo de respuesta constante cuando el
# usuario no existe o está inactivo, evitando enumeración por timing.
_DUMMY_HASH = "$2b$12$CjqYb0yF3lGz9m2vB0nGwuKAzKQoRl9XkQxg3zZ9x0EJf5F0rXK1a"

MAX_INTENTOS = 5
BLOQUEO_MINUTOS = 15
_intentos_fallidos: dict[str, tuple[int, datetime | None]] = {}


def _bloqueado(usuario: str) -> bool:
    intentos, bloqueado_hasta = _intentos_fallidos.get(usuario, (0, None))
    if bloqueado_hasta and datetime.now(timezone.utc) < bloqueado_hasta:
        return True
    return False


def _registrar_intento_fallido(usuario: str) -> None:
    intentos, _ = _intentos_fallidos.get(usuario, (0, None))
    intentos += 1
    bloqueado_hasta = None
    if intentos >= MAX_INTENTOS:
        bloqueado_hasta = datetime.now(timezone.utc) + timedelta(minutes=BLOQUEO_MINUTOS)
    _intentos_fallidos[usuario] = (intentos, bloqueado_hasta)


def _limpiar_intentos(usuario: str) -> None:
    _intentos_fallidos.pop(usuario, None)


class LoginRequest(BaseModel):
    usuario: str
    password: str


class UsuarioOut(BaseModel):
    id_usuario: int
    loguin_usuario: str
    rol: str


class LoginResponse(BaseModel):
    access_token: str
    usuario: UsuarioOut


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_auth_db)):
    usuario_normalizado = payload.usuario.strip().lower()

    if _bloqueado(usuario_normalizado):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos fallidos. Intente nuevamente en {BLOQUEO_MINUTOS} minutos",
        )

    user = db.query(Usuario).filter(Usuario.loguin_usuario == payload.usuario).first()

    # Siempre se ejecuta verify_password (contra el hash real o uno dummy)
    # para que el tiempo de respuesta no delate si el usuario existe.
    password_hash = user.password_hash if user else _DUMMY_HASH
    password_ok = verify_password(payload.password, password_hash)

    if not user or not user.activo or not password_ok:
        _registrar_intento_fallido(usuario_normalizado)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

    _limpiar_intentos(usuario_normalizado)

    token = create_access_token({"sub": user.loguin_usuario, "id_usuario": user.id_usuario, "rol": user.rol})

    return LoginResponse(
        access_token=token,
        usuario=UsuarioOut(id_usuario=user.id_usuario, loguin_usuario=user.loguin_usuario, rol=user.rol),
    )
