from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.core.database import Base


class MailEnvioMasivo(Base):
    """Job de envío masivo de mail procesado en background."""
    __tablename__ = "mail_envios_masivos"

    id_envio = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, nullable=False)
    tipo_mensaje = Column(String(50), nullable=False)
    origen = Column(String(10), nullable=False)  # 'csv' | 'cuentas'
    total = Column(Integer, nullable=False, default=0)
    enviados = Column(Integer, nullable=False, default=0)
    errores = Column(Integer, nullable=False, default=0)
    descartados_sin_cliente = Column(Integer, nullable=False, default=0)
    descartados_duplicados = Column(Integer, nullable=False, default=0)
    estado = Column(String(20), nullable=False, default="pendiente")
    creado_at = Column(DateTime, nullable=False, default=datetime.now)
    finalizado_at = Column(DateTime, nullable=True)


class RegistroEnvioMail(Base):
    """Log de envíos de mail (individual y masivo) — mismo rol que registro_envios_whatsapp."""
    __tablename__ = "registro_envios_mail"

    id = Column(Integer, primary_key=True)
    matricula = Column(String(50), nullable=True)
    cuentas_id_cta = Column(Integer, nullable=True)
    destino = Column(String(250), nullable=True)
    asunto = Column(String(250), nullable=True)
    mensaje = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=True)
    id_usuario = Column(Integer, nullable=True)
    estado = Column(String(255), nullable=True)
    fecha_envio = Column(DateTime, nullable=True)
    envio_masivo_id = Column(Integer, nullable=True)
