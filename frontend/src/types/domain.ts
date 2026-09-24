// Reflejan 1:1 los schemas Pydantic reales de backend-api (src/models/schemas.py)

export interface CuentaOut {
  id_cta: number;
  entidades_matricula_ent: string;
  estados_id_estado: number | null;
  sub_estados_id_sub_est: number | null;
  cuenta_cliente: string | null;
  deudatrans_cta: string | null;
  deudaact_cta: string | null;
  fechaingreso_cta: string | null;
  empleador_cta: string | null;
  activa_cta: string | null;
  judicial: string | null;
  observacion_cta: string | null;
  razon_social_ent: string | null;
}

export interface EntidadOut {
  matricula_ent: string;
  razon_social_ent: string | null;
  contacto_ent: string | null;
  activo_ent: string | null;
  genero: string | null;
}

export interface TelefonoOut {
  id_tel: number;
  tipo_tel: string | null;
  codigo_area_tel: string | null;
  numero_tel: string | null;
  observaciones_tel?: string | null;
  activo_tel: string | null;
}

export interface DireccionOut {
  id_dir: number;
  calle_dir: string | null;
  nro_dir: string | null;
  piso_dir?: string | null;
  dpto_dir?: string | null;
  barrio_dir: string | null;
  cp_dir?: string | null;
  localidad_dir: string | null;
  departamento_dir?: string | null;
  provincia_dir: string | null;
  tipo_dir?: string | null;
  observacion_dir?: string | null;
  activa_dir: string | null;
}

export interface MailOut {
  mail: string | null;
  tipo_mail: string | null;
  activo_mail: string | null;
}

// Devuelto por el ABM /entidades/{matricula}/mails (incluye id_mails).
export interface MailAbmOut {
  id_mails: number;
  mail: string | null;
  tipo_mail: string | null;
  activo_mail: string | null;
}

// Catálogos para el ABM de contactos de gestión.
export interface AccionOut {
  id_accion: number;
  desc_accion: string;
}

export interface ResultadoOut {
  id_resultado: number;
  desc_resultado: string;
}

export interface CuentaDetalleOut extends CuentaOut {
  estado_desc: string | null;
  sub_estado_desc: string | null;
  cliente_desc: string | null;
  subcliente_nombre: string | null;
  entidad: EntidadOut | null;
  telefonos: TelefonoOut[];
  direcciones: DireccionOut[];
  mails: MailOut[];
}

export interface ContactoOut {
  id_contacto: number;
  fecha_contacto: string | null;
  hora_contacto: string | null;
  resultados_id_resultado: number;
  acciones_id_accion: number;
  nota_contacto?: string | null;
  usuario_nombre?: string | null;
  activo: string | null;
}

export interface ConceptoCobroOut {
  id_concepto: number;
  desc_concepto: string;
}

export interface CobroOut {
  id_cobros: number;
  cuentas_id_cta: number;
  fcha_cobro: string | null;
  concepto: string | null;
  importe: string | null;
  rendido: string | null;
  anulado: string | null;
  anulado_por_nombre?: string | null;
  anulado_ts?: string | null;
}

export interface FilaInformeCobro {
  id_cobros: number;
  fecha: string | null;
  id_cta: number;
  matricula: string | null;
  razon_social: string | null;
  concepto: string | null;
  importe: string | null;
  rendido: string | null;
  anulado: string | null;
}

export interface ConvenioOut {
  id_convenios: number;
  fecha_convenio: string | null;
  estado_convenio: string | null;
  importe_convenio: string | null;
  anticipo_convenio: string | null;
  cant_cuotas_convenio: number | null;
  importe_cuota_convenio: string | null;
  cuotas_pagadas: number | null;
  saldo_convenio: string | null;
  observaciones_convenio?: string | null;
  cancelado: string | null;
  activo: string | null;
}

export interface ReciboOut {
  nro_recibo: number;
  id_cta: number;
  fcha_cobro: string | null;
  nombre: string | null;
  domicilio: string | null;
  localidad: string | null;
  telefono: string | null;
  subcliente: string | null;
  concepto: string;
  cuota: number | null;
  cant_cuotas: number | null;
  importe: string;
  importe_de_letras: string;
}

export interface Usuario {
  id_usuario: number;
  loguin_usuario: string;
  rol: string;
}

export interface AgendaOut {
  id_agenda: number;
  cuentas_id_cta: number;
  usuarios_id_usuario: number;
  desc_agenda: string | null;
  fecha_agenda: string | null;
  activo: string | null;
}

export interface VencimientoOut {
  id_vto: number;
  id_cta: number;
  id_convenio: number;
  fecha: string;
  nro_cuota: number;
  monto: string | null;
  descripcion: string | null;
  fecha_pago: string;
  pagado: string | null;
}

// Carga masiva / cambios masivos (Asistente IA).
export interface SubEstadoOut {
  id_sub_est: number;
  desc_sub_est: string;
}

export interface EjecutivoOut {
  id_usuario: number;
  nombre: string;
}

export interface CargaMasivaResult {
  entidad?: string;
  insertadas: number;
  errores: { fila: number; motivo: string }[];
}

export interface ProcesarCargaResult {
  promovidas: number;
  errores: { fila: number; motivo: string }[];
  restantes: number;
}

export interface CambioMasivoResult {
  afectadas: number;
  no_encontradas: string[];
}

// Asistente IA — analista de cobranza extrajudicial.
export interface SenalesPrioridad {
  judicial_activa: boolean;
  convenio_caido: boolean;
  promesa_incumplida: boolean;
}

export interface PrioridadCuenta {
  id_cta: number;
  nombre: string;
  deuda: number;
  score_prioridad: number;
  nivel_prioridad: string;
  "señales": SenalesPrioridad;
}

export interface SenalesCuenta {
  antiguedad_dias: number;
  gestiones_previas: number;
  gestiones_sin_resultado: number;
  promesa_incumplida: boolean;
  convenio_caido: boolean;
  judicial_activa: boolean;
}

export interface ComplianceHorario {
  horario_ok: boolean;
  motivo: string | null;
  ya_contactado_hoy: boolean;
}

export interface PlanSugerido {
  cant_cuotas: number;
  anticipo_sugerido: number;
  importe_cuota: number;
}

export interface EstrategiaCuenta {
  id_cta: number;
  nombre: string;
  deuda: number;
  score_prioridad: number;
  nivel_prioridad: string;
  "señales": SenalesCuenta;
  compliance: ComplianceHorario;
  plan_sugerido: PlanSugerido;
  proxima_accion: string;
}

export interface GenerarMensajeResult {
  mensaje: string;
  plan_sugerido?: PlanSugerido;
  advertencia?: string;
}
