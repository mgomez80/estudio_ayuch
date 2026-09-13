"""
Núcleo del sistema: quién debe (entidades), cuánto y en qué estado (cuentas),
y para quién se gestiona la cobranza (clientes / subclientes).
"""
from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship, foreign
from src.core.database import Base


class Entidad(Base):
    """Persona/deudor. La PK real es la matrícula (DNI/CUIT), no un id autoincremental."""
    __tablename__ = "entidades"

    matricula_ent = Column(String(30), primary_key=True)
    tipo_matricula_id_tipomatricula = Column(Integer)
    condicion_iva_id_cond_iva = Column(Integer)
    razon_social_ent = Column(String(200))
    contacto_ent = Column(String(20))
    activo_ent = Column(String(1), default="S")
    genero = Column(String(1))

    cuentas = relationship(
        "Cuenta",
        primaryjoin="Entidad.matricula_ent==foreign(Cuenta.entidades_matricula_ent)",
        viewonly=True,
    )
    telefonos = relationship(
        "Telefono",
        primaryjoin="Entidad.matricula_ent==foreign(Telefono.entidades_matricula_ent)",
        viewonly=True,
    )
    direcciones = relationship(
        "Direccion",
        primaryjoin="Entidad.matricula_ent==foreign(Direccion.entidades_matricula_ent)",
        viewonly=True,
    )
    mails = relationship(
        "Mail",
        primaryjoin="Entidad.matricula_ent==foreign(Mail.entidades_matricula_ent)",
        viewonly=True,
    )


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    cuenta_cliente = Column(Integer, primary_key=True)
    desc_cliente = Column(String(200))
    activo = Column(String(1), default="S")


class Subcliente(Base):
    __tablename__ = "subclientes"

    id_subcli = Column(Integer, primary_key=True)
    clientes_id_cliente = Column(Integer, nullable=False)
    clientes_cuenta_cliente = Column(Integer, nullable=False)
    nombre_subcli = Column(String(100))
    decuento_subcli = Column(DECIMAL(10, 0))
    porccomi_subcli = Column(DECIMAL(10, 0))
    porcquita_subcli = Column(DECIMAL(10, 0))
    porcact_subcli = Column(DECIMAL(10, 0))
    plazogestion_subcli = Column(Integer)
    activo_subcli = Column(String(1), default="S")


class Cuenta(Base):
    """La deuda en sí: vincula una entidad con un estado, un subcliente, y montos."""
    __tablename__ = "cuentas"

    id_cta = Column(Integer, primary_key=True)
    estados_id_estado = Column(Integer)
    sub_estados_id_sub_est = Column(Integer)
    entidades_matricula_ent = Column(String(30), nullable=False)
    cuenta_cliente = Column(String(50))
    subclientes_id_subcli = Column(Integer, nullable=False)
    deudatrans_cta = Column(DECIMAL(10, 2))
    deudaact_cta = Column(DECIMAL(10, 2))
    fechaingreso_cta = Column(Date)
    fecha_padron_cta = Column(String(12))
    fecha_asignacion_cta = Column(String(12))
    empleador_cta = Column(String(200))
    activa_cta = Column(String(1), default="S")
    supervisor = Column(Integer)
    observacion_cta = Column(String(250))
    ejecutivo = Column(Integer)
    judicial = Column(String(1), default="N")
    promo = Column(String(1))
    descripcion_promo = Column(String(200))

    entidad = relationship(
        "Entidad",
        primaryjoin="foreign(Cuenta.entidades_matricula_ent)==Entidad.matricula_ent",
        viewonly=True,
    )
