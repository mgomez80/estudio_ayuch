from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.core.auth_database import get_auth_db
from src.core.security import verify_password, create_access_token
from src.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])


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
    user = db.query(Usuario).filter(Usuario.loguin_usuario == payload.usuario).first()

    if not user or not user.activo or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

    token = create_access_token({"sub": user.loguin_usuario, "id_usuario": user.id_usuario, "rol": user.rol})

    return LoginResponse(
        access_token=token,
        usuario=UsuarioOut(id_usuario=user.id_usuario, loguin_usuario=user.loguin_usuario, rol=user.rol),
    )
