from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from src.core.database import Base


class GestorChatSesion(Base):
    __tablename__ = "gestor_chat_sesiones"

    id_sesion = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False, index=True)
    titulo = Column(String(200))
    creado_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class GestorChatMensaje(Base):
    __tablename__ = "gestor_chat_mensajes"

    id_mensaje = Column(Integer, primary_key=True, autoincrement=True)
    id_sesion = Column(Integer, nullable=False, index=True)
    rol = Column(String(20), nullable=False)
    contenido = Column(Text)
    tool_calls_json = Column(Text)
    creado_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class GestorAccion(Base):
    __tablename__ = "gestor_acciones"

    id_accion = Column(Integer, primary_key=True, autoincrement=True)
    id_sesion = Column(Integer, nullable=False, index=True)
    id_usuario = Column(Integer, nullable=False)
    tool_name = Column(String(50), nullable=False)
    argumentos_json = Column(Text, nullable=False)
    estado = Column(String(20), nullable=False)
    resultado_json = Column(Text)
    creado_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    resuelto_at = Column(DateTime)


class GestorInforme(Base):
    __tablename__ = "gestor_informes"

    id_informe = Column(Integer, primary_key=True, autoincrement=True)
    id_sesion = Column(Integer, index=True)
    id_usuario = Column(Integer, nullable=False, index=True)
    tipo = Column(String(30), nullable=False)
    titulo = Column(String(200), nullable=False)
    parametros_json = Column(Text)
    html = Column(Text, nullable=False)
    creado_at = Column(DateTime, nullable=False, default=datetime.utcnow)
