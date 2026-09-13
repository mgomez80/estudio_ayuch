/** Formatea fechas ISO (aaaa-mm-dd o datetime) como dd/mm/aaaa. Devuelve "—" si no hay valor. */
export function fmtFecha(v: string | null | undefined): string {
  if (!v) return "—";
  const m = String(v).match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return String(v);
  return `${m[3]}/${m[2]}/${m[1]}`;
}

/** dd/mm/aaaa hh:mm para datetimes; cae a fmtFecha si no trae hora. */
export function fmtFechaHora(v: string | null | undefined): string {
  if (!v) return "—";
  const m = String(v).match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})/);
  if (!m) return fmtFecha(v);
  return `${m[3]}/${m[2]}/${m[1]} ${m[4]}:${m[5]}`;
}
