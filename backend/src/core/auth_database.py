from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from src.core.database import Base


class AuthSettings(BaseSettings):
    auth_db_host: str
    auth_db_port: int = 3306
    auth_db_name: str
    auth_db_user: str
    auth_db_password: str

    class Config:
        env_file = ".env"
        extra = "ignore"


auth_settings = AuthSettings()

AUTH_DATABASE_URL = (
    f"mysql+pymysql://{auth_settings.auth_db_user}:{auth_settings.auth_db_password}"
    f"@{auth_settings.auth_db_host}:{auth_settings.auth_db_port}/{auth_settings.auth_db_name}?charset=utf8mb4"
)

auth_engine = create_engine(AUTH_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)


def get_auth_db():
    """Dependency de FastAPI: sesión sobre db_cobranza_test (tabla usuarios)."""
    db = AuthSessionLocal()
    try:
        yield db
    finally:
        db.close()
