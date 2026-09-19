from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

DATABASE_URL = (
    f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}?charset=utf8mb4"
)

# pool_pre_ping evita errores por conexiones muertas (MySQL cierra conexiones inactivas)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency de FastAPI: entrega una sesión de DB y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
