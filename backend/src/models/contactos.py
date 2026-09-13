from sqlalchemy import Column, Integer, String, Date, LargeBinary
from src.core.database import Base


class Telefono(Base):
    __tablename__ = "telefonos"

    id_tel = Column(Integer, primary_key=True)
    entidades_matricula_ent = Column(String(30), nullable=False)
    tipo_tel = Column(String(50))
    codigo_area_tel = Column(String(6))
    numero_tel = Column(String(50))
    observaciones_tel = Column(String(250))
    activo_tel = Column(String(1), default="S")


class Direccion(Base):
    __tablename__ = "direcciones"

    id_dir = Column(Integer, primary_key=True)
    entidades_matricula_ent = Column(String(30), nullable=False)
    calle_dir = Column(String(200))
    nro_dir = Column(String(100))
    piso_dir = Column(String(10))
    dpto_dir = Column(String(10))
    barrio_dir = Column(String(200))
    cp_dir = Column("CP_dir", String(20))
    localidad_dir = Column(String(200))
    departamento_dir = Column(String(100))
    provincia_dir = Column(String(200))
    activa_dir = Column(String(1), default="S")
    tipo_dir = Column(String(50))
    observacion_dir = Column(String(100))


class Mail(Base):
    __tablename__ = "mails"

    id_mails = Column(Integer, primary_key=True)
    entidades_matricula_ent = Column(String(30), nullable=False)
    mail = Column(String(250))
    tipo_mail = Column(String(50))
    activo_mail = Column(String(1), default="S")


class Contacto(Base):
    """Historial de gestión de cobranza (llamadas, whatsapp, etc.) sobre una cuenta."""
    __tablename__ = "contactos"

    id_contacto = Column(Integer, primary_key=True)
    usuarios_id_usuario = Column(Integer, nullable=False)
    cuentas_id_cta = Column(Integer, nullable=False)
    resultados_id_resultado = Column(Integer, nullable=True)
    acciones_id_accion = Column(Integer, nullable=True)
    fecha_contacto = Column(Date)
    hora_contacto = Column(String(10))
    nota_contacto = Column(LargeBinary)
    activo = Column(String(1))


class ContactoJudicial(Base):
    __tablename__ = "contactos_judiciales"

    id_contacto_judicial = Column(Integer, primary_key=True)
    usuarios_id_usuario = Column(Integer, nullable=False)
    cuentas_id_cta = Column(Integer, nullable=False)
    resultados_id_resultado = Column(Integer, nullable=True)
    acciones_id_accion = Column(Integer, nullable=True)
    fecha_contacto = Column(Date)
    hora_contacto = Column(String(10))
    nota_contacto = Column(LargeBinary)
    fecha_inicio_caducidad = Column(Date)
    activo = Column(String(1))


class Agenda(Base):
    __tablename__ = "agenda"

    id_agenda = Column(Integer, primary_key=True)
    usuarios_id_usuario = Column(Integer, nullable=False)
    cuentas_id_cta = Column(Integer, nullable=False)
    desc_agenda = Column(String(250))
    fecha_agenda = Column(Date)
    activo = Column(String(1))
