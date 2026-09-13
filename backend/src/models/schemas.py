"""
Schemas Pydantic: definen la forma de los datos que devuelve la API (no son las tablas
de la DB, son la "vista" que exponemos hacia afuera).
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from src.core.numeros import normalizar_deuda as _normalizar_deuda


class EntidadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    matricula_ent: str
    razon_social_ent: Optional[str] = None
    contacto_ent: Optional[str] = None
    activo_ent: Optional[str] = None
    genero: Optional[str] = None


class TelefonoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_tel: int
    tipo_tel: Optional[str] = None
    codigo_area_tel: Optional[str] = None
    numero_tel: Optional[str] = None
    activo_tel: Optional[str] = None


class DireccionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_dir: int
    calle_dir: Optional[str] = None
    nro_dir: Optional[str] = None
    barrio_dir: Optional[str] = None
    localidad_dir: Optional[str] = None
    provincia_dir: Optional[str] = None
    activa_dir: Optional[str] = None


class MailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mail: Optional[str] = None
    tipo_mail: Optional[str] = None
    activo_mail: Optional[str] = None


class CuentaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cta: int
    entidades_matricula_ent: str
    estados_id_estado: Optional[int] = None
    sub_estados_id_sub_est: Optional[int] = None
    cuenta_cliente: Optional[str] = None
    deudatrans_cta: Optional[Decimal] = None
    deudaact_cta: Optional[Decimal] = None
    fechaingreso_cta: Optional[date] = None
    empleador_cta: Optional[str] = None
    activa_cta: Optional[str] = None
    judicial: Optional[str] = None
    observacion_cta: Optional[str] = None
    razon_social_ent: Optional[str] = None

    _norm_deuda = field_validator("deudatrans_cta", "deudaact_cta", mode="before")(_normalizar_deuda)


class CuentaDetalleOut(CuentaOut):
    estado_desc: Optional[str] = None
    sub_estado_desc: Optional[str] = None
    cliente_desc: Optional[str] = None
    subcliente_nombre: Optional[str] = None
    entidad: Optional[EntidadOut] = None
    telefonos: list[TelefonoOut] = []
    direcciones: list[DireccionOut] = []
    mails: list[MailOut] = []


class ContactoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_contacto: int
    fecha_contacto: Optional[date] = None
    hora_contacto: Optional[str] = None
    resultados_id_resultado: Optional[int] = None
    acciones_id_accion: Optional[int] = None
    activo: Optional[str] = None
    desc_accion: Optional[str] = None
    desc_resultado: Optional[str] = None
    usuario_nombre: Optional[str] = None
    nota_contacto: Optional[str] = None


class ConvenioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_convenios: int
    fecha_convenio: Optional[date] = None
    estado_convenio: Optional[str] = None
    importe_convenio: Optional[Decimal] = None
    anticipo_convenio: Optional[Decimal] = None
    cant_cuotas_convenio: Optional[int] = None
    importe_cuota_convenio: Optional[Decimal] = None
    cuotas_pagadas: Optional[int] = None
    saldo_convenio: Optional[Decimal] = None
    cancelado: Optional[str] = None
    activo: Optional[str] = None


class CobroOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cobros: int
    fcha_cobro: Optional[date] = None
    desc_cobro: Optional[str] = None
    importe: Optional[Decimal] = None
    cuota: Optional[int] = None
    rendido: Optional[str] = None
    movimientos_id_mov: Optional[int] = None
    convenios_id_convenios: Optional[int] = None
    anulado: Optional[str] = None
    anulado_por: Optional[int] = None
    anulado_ts: Optional[datetime] = None
    anulado_por_nombre: Optional[str] = None
    concepto: Optional[str] = None


class AgendaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_agenda: int
    cuentas_id_cta: int
    usuarios_id_usuario: int
    desc_agenda: Optional[str] = None
    fecha_agenda: Optional[date] = None
    activo: Optional[str] = None


class AgendaCreate(BaseModel):
    desc_agenda: str
    fecha_agenda: date
    usuarios_id_usuario: Optional[int] = None  # si no viene, se agenda al usuario logueado


class AgendaUpdate(BaseModel):
    desc_agenda: Optional[str] = None
    fecha_agenda: Optional[date] = None
    usuarios_id_usuario: Optional[int] = None


class VencimientoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_vto: int
    id_cta: int
    id_convenio: int
    fecha: date
    nro_cuota: int
    monto: Optional[Decimal] = None
    descripcion: Optional[str] = None
    fecha_pago: date
    pagado: Optional[str] = None


class VencimientoCreate(BaseModel):
    id_convenio: int
    fecha: date
    nro_cuota: int
    monto: Optional[Decimal] = None
    descripcion: Optional[str] = None
    fecha_pago: date


class VencimientoUpdate(BaseModel):
    fecha: Optional[date] = None
    nro_cuota: Optional[int] = None
    monto: Optional[Decimal] = None
    descripcion: Optional[str] = None
