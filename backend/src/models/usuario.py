from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from src.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    loguin_usuario = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(150))
    rol = Column(String(50), nullable=False, default="admin")
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, server_default=func.now())
    perfiles_id_perfil = Column(Integer, nullable=True)
