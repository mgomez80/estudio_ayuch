"""
Tablas de catálogo: valores fijos que se usan como referencia en otras tablas.
Todas son de solo lectura desde la API por ahora (se cargan una vez y rara vez cambian).
"""
from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Estado(Base):
    __tablename__ = "estados"

    id_estado = Column(Integer, primary_key=True)
    desc_estado = Column(String(254))
    tipo_estado = Column(String(50))  # POSITIVO / NEGATIVO / JUDICIAL
    activo = Column(String(1))


class SubEstado(Base):
    __tablename__ = "sub_estados"

    id_sub_est = Column(Integer, primary_key=True)
    estados_id_estado = Column(Integer, nullable=False)
    desc_sub_est = Column(String(254))
    activo = Column(String(1))


class Resultado(Base):
    __tablename__ = "resultados"

    id_resultado = Column(Integer, primary_key=True)
    desc_resultado = Column(String(254))
    positivo = Column(String(1))
    activo = Column(String(1))


class Accion(Base):
    __tablename__ = "acciones"

    id_accion = Column(Integer, primary_key=True)
    desc_accion = Column(String(250))
    activa = Column(String(1))


class Rubro(Base):
    __tablename__ = "rubros"

    id_rubro = Column(Integer, primary_key=True)
    desc_rubro = Column(String(250))
    activo = Column(String(1))


class Concepto(Base):
    __tablename__ = "conceptos"

    id_concepto = Column(Integer, primary_key=True)
    rubros_id_rubro = Column(Integer, nullable=False)
    desc_concepto = Column(String(254))
    activo = Column(String(1))


class Provincia(Base):
    __tablename__ = "provincias"

    id_provincia = Column(Integer, primary_key=True)
    nombre_provincia = Column(String(50))


class TipoMatricula(Base):
    __tablename__ = "tipo_matricula"

    id_tipomatricula = Column(Integer, primary_key=True)
    detalle_tipomatricula = Column(String(10))


class CondicionIva(Base):
    __tablename__ = "condicion_iva"

    id_cond_iva = Column(Integer, primary_key=True)
    detalle = Column(String(50))
    porcentaje = Column(Integer)


class Modulo(Base):
    __tablename__ = "modulos"

    id_modulo = Column(Integer, primary_key=True)
    clave = Column(String(50), nullable=False, unique=True)
    desc_modulo = Column(String(100), nullable=False)


class Perfil(Base):
    __tablename__ = "perfiles"

    id_perfil = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    activo = Column(String(1), nullable=False, default="S")


class PerfilPermiso(Base):
    __tablename__ = "perfil_permisos"

    perfiles_id_perfil = Column(Integer, primary_key=True, nullable=False)
    modulos_id_modulo = Column(Integer, primary_key=True, nullable=False)
    ver = Column(String(1), nullable=False, default="N")
    alta = Column(String(1), nullable=False, default="N")
    baja = Column(String(1), nullable=False, default="N")
    modificar = Column(String(1), nullable=False, default="N")
