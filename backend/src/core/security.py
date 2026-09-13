import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480  # 8 horas de sesión

    class Config:
        env_file = ".env"
        extra = "ignore"


jwt_settings = JWTSettings()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), password_hash.encode())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.jwt_expire_minutes)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, jwt_settings.jwt_secret, algorithm=jwt_settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, jwt_settings.jwt_secret, algorithms=[jwt_settings.jwt_algorithm])


_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    try:
        return decode_access_token(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")


def get_current_admin(
    user: dict = Depends(get_current_user),
) -> dict:
    if user.get("rol") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requiere rol admin")
    return user
