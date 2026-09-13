from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.core.database import Base


class WaConversacion(Base):
    __tablename__ = "wa_conversaciones"

    id_conv = Column(Integer, primary_key=True)
    telefono = Column(String(30), nullable=False, unique=True)
    nombre_contacto = Column(String(200), nullable=True)
    cuentas_id_cta = Column(Integer, nullable=True)
    ultimo_mensaje = Column(String(500), nullable=True)
    ultimo_mensaje_at = Column(DateTime, nullable=True)
    no_leidos = Column(Integer, nullable=False, default=0)
    estado = Column(String(20), nullable=False, default="abierta")
    creado_at = Column(DateTime, nullable=False, default=datetime.now)


class WaMensaje(Base):
    __tablename__ = "wa_mensajes"

    id_msg = Column(Integer, primary_key=True)
    conversaciones_id_conv = Column(Integer, nullable=False)
    direccion = Column(String(3), nullable=False)  # 'in' o 'out'
    texto = Column(Text, nullable=True)
    tipo = Column(String(20), nullable=False, default="text")
    media_url = Column(String(500), nullable=True)
    ycloud_id = Column(String(100), nullable=True)
    estado = Column(String(20), nullable=False, default="pendiente")
    usuarios_id_usuario = Column(Integer, nullable=True)
    creado_at = Column(DateTime, nullable=False, default=datetime.now)
    eliminado = Column(Integer, nullable=False, default=0)
    editado = Column(Integer, nullable=False, default=0)
    editado_en = Column(DateTime, nullable=True)
    leido_at = Column(DateTime, nullable=True)
    leido_por = Column(Integer, nullable=True)
    media_id = Column(String(255), nullable=True)
    archivo_nombre = Column(String(200), nullable=True)
    media_mime = Column(String(100), nullable=True)
    texto_original = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    error_msg = Column(String(500), nullable=True)
    eliminado_en = Column(DateTime, nullable=True)


class RegistroEnvioWhatsapp(Base):
    """Log de envíos (individual y masivo) — mismo rol que la tabla legacy."""
    __tablename__ = "registro_envios_whatsapp"

    id = Column(Integer, primary_key=True)
    matricula = Column(String(50), nullable=True)
    cuentas_id_cta = Column(Integer, nullable=True)
    destino = Column(String(20), nullable=True)
    mensaje = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=True)
    id_usuario = Column(Integer, nullable=True)
    estado = Column(String(255), nullable=True)
    fecha_envio = Column(DateTime, nullable=True)
    envio_masivo_id = Column(Integer, nullable=True)
    ycloud_id = Column(String(100), nullable=True)


class WaEnvioMasivo(Base):
    """Job de envío masivo procesado en background."""
    __tablename__ = "wa_envios_masivos"

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


class WhatsappAutoreplyControl(Base):
    """Control de autoreply para evitar spam."""
    __tablename__ = "whatsapp_autoreply_control"

    telefono = Column(String(30), primary_key=True)
    ultimo_envio = Column(DateTime, nullable=True)
    veces = Column(Integer, nullable=False, default=1)
