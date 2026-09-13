from sqlalchemy import Column, Integer, String, Date, DECIMAL
from src.core.database import Base


class Demanda(Base):
    __tablename__ = "demandas"

    id_demanda = Column(Integer, primary_key=True)
    caratula = Column(String(250))
    expediente = Column(String(250))
    secretarias_id_secretaria = Column(Integer)
    juzgados_id_juzgado = Column(Integer)
    monto_demanda = Column(DECIMAL(10, 2))
    apoderado = Column(String(40))
    fecha_inicio_demanda = Column(String(20))
    fecha_mora = Column(String(20))
    cuentas_id_cta = Column(Integer)
    fecha_inicio_caducidad = Column(String(20))
    activa = Column(String(1), default="S")


class Juzgado(Base):
    __tablename__ = "juzgados"

    id_juzgado = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    detalle = Column(String(200))


class Secretaria(Base):
    __tablename__ = "secretarias"

    id_secretaria = Column(Integer, primary_key=True)
    nombre = Column(String(50))


class GastoJudicial(Base):
    __tablename__ = "gastos_judiciales"

    id_gasto_judicial = Column(Integer, primary_key=True)
    bono_profesional = Column(DECIMAL(10, 2))
    tasa_judicial = Column(Integer)
    monto_tasa_judicial = Column(DECIMAL(10, 2))
    planilla_fiscal = Column(DECIMAL(10, 2))
    movilidad = Column(DECIMAL(10, 2))
    fotocopias = Column(DECIMAL(10, 2))
    sellado = Column(DECIMAL(10, 2))
    diligencias = Column(DECIMAL(10, 2))
    otros = Column(DECIMAL(10, 2))
    observaciones = Column(String(250))
    cuentas_id_cta = Column(String(20))
    fecha = Column(Date)


class PagoJudicial(Base):
    __tablename__ = "pagos_judiciales"

    id_pago_judicial = Column(Integer, primary_key=True)
    importe = Column(DECIMAL(10, 2))
    detalle = Column(String(250))
    gastos_pendientes = Column(DECIMAL(10, 2))
    fecha = Column(Date)
    cuentas_id_cta = Column(Integer)
    id_mov = Column(Integer)
    cancelado = Column(String(1))
    id_concepto = Column(Integer)
    concepto_cobro = Column(Integer)
    cuota = Column(Integer)


class TasaDeJusticia(Base):
    __tablename__ = "tasas_de_justicia"

    id_tasa = Column(Integer, primary_key=True)
    nombre = Column(String(20))
    valor = Column(DECIMAL(10, 2))
