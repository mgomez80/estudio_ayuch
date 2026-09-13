from sqlalchemy import Column, Integer, String, Date, DateTime, DECIMAL
from src.core.database import Base


class Propuesta(Base):
    __tablename__ = "propuestas"

    id_propuesta = Column(Integer, primary_key=True)
    contactos_id_contacto = Column(Integer, nullable=False)
    cuentas_id_cta = Column(Integer, nullable=False)
    fecha_propuesta = Column(Date)
    concepto_propuesta = Column(String(100))
    fechavto_propuesta = Column(Date)
    estado_propuesta = Column(String(100))
    activa = Column(String(1))


class Convenio(Base):
    """Plan de pago acordado con el deudor."""
    __tablename__ = "convenios"

    id_convenios = Column(Integer, primary_key=True)
    cuentas_id_cta = Column(Integer, nullable=False)
    propuestas_id_propuesta = Column(Integer, nullable=False)
    fecha_convenio = Column(Date)
    concepto_convenio = Column(Integer)
    estado_convenio = Column(String(50))
    importe_convenio = Column(DECIMAL(10, 2))
    anticipo_convenio = Column(DECIMAL(10, 2))
    cant_cuotas_convenio = Column(Integer)
    importe_cuota_convenio = Column(DECIMAL(10, 2))
    cuotas_pagadas = Column(Integer)
    saldo_convenio = Column(DECIMAL(10, 2))
    observaciones_convenio = Column(String(254))
    cancelado = Column(String(1))
    activo = Column(String(1))


class ConvenioJudicial(Base):
    __tablename__ = "convenios_judiciales"

    id_convenios_judiciales = Column(Integer, primary_key=True)
    cuentas_id_cta = Column(Integer, nullable=False)
    propuestas_id_propuesta = Column(Integer, nullable=False)
    fecha_convenio = Column(Date)
    concepto_convenio = Column(Integer)
    estado_convenio = Column(String(50))
    importe_convenio = Column(DECIMAL(10, 2))
    anticipo_convenio = Column(DECIMAL(10, 2))
    cant_cuotas_convenio = Column(Integer)
    importe_cuota_convenio = Column(DECIMAL(10, 2))
    cuotas_pagadas = Column(Integer)
    saldo_convenio = Column(DECIMAL(10, 2))
    observaciones_convenio = Column(String(254))
    cancelado = Column(String(1))
    activo = Column(String(1))


class Vencimiento(Base):
    """Cuotas individuales de un convenio, con su fecha de vencimiento y si se pagó."""
    __tablename__ = "vencimientos"

    id_vto = Column(Integer, primary_key=True)
    id_cta = Column(Integer, nullable=False)
    id_convenio = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    nro_cuota = Column(Integer, nullable=False)
    monto = Column(DECIMAL(10, 2))
    descripcion = Column(String(300))
    fecha_pago = Column(Date, nullable=False)
    pagado = Column(String(1), default="N")


class Movimiento(Base):
    """Caja: ingresos y egresos generales."""
    __tablename__ = "movimientos"

    id_mov = Column(Integer, primary_key=True)
    importe_ingreso_mov = Column(DECIMAL(10, 2))
    importe_egreso_mov = Column(DECIMAL(10, 2))
    fecha_mov = Column(Date)
    desc_mov = Column(String(254))
    anulado_mov = Column(String(1), default="N")


class Cobro(Base):
    """Un pago efectivamente recibido, vinculado a un movimiento de caja y una cuenta."""
    __tablename__ = "cobros"

    id_cobros = Column(Integer, primary_key=True)
    movimientos_id_mov = Column(Integer, nullable=False)
    conceptos_id_concepto = Column("CONCEPTOS_id_concepto", Integer, nullable=False)
    concepto_cobro = Column(Integer)
    cuentas_id_cta = Column(Integer, nullable=False)
    convenios_id_convenios = Column(Integer)
    fcha_cobro = Column(Date)
    cuota = Column(Integer)
    desc_cobro = Column(String(250))
    importe = Column(DECIMAL(10, 2))
    rendido = Column(String(1))
    # Trazabilidad de anulación (soft-delete): nunca se borra un cobro de la DB
    anulado = Column(String(1), default="N")
    anulado_por = Column(Integer)
    anulado_ts = Column(DateTime)


class Gasto(Base):
    __tablename__ = "gastos"

    id_gastos = Column(Integer, primary_key=True)
    movimientos_id_mov = Column(Integer, nullable=False)
    fcha_gasto = Column(Date)
    desc_gasto = Column(String(254))
    importe_gasto = Column(DECIMAL(10, 2))
    activo = Column(String(1))


class PagoComision(Base):
    __tablename__ = "pago_comisiones"

    id_pago_com = Column(Integer, primary_key=True)
    movimientos_id_mov = Column(Integer, nullable=False)
    subclientes_id_subcli = Column(Integer, nullable=False)
    importe_comision = Column(DECIMAL(10, 2))
    fecha_pago_comision = Column(Date)
    mes_de_comision = Column(String(20))


class Rendido(Base):
    __tablename__ = "rendidos"

    id_rendido = Column(Integer, primary_key=True)
    movimientos_id_mov = Column(Integer, nullable=False)
    subclientes_id_subcli = Column(Integer, nullable=False)
    cobros_id_cobros = Column(Integer, nullable=False)
    fecha_rendido = Column(Date)
    importe_rendido = Column(DECIMAL(10, 2))
    periodo_rendido = Column(String(40))
