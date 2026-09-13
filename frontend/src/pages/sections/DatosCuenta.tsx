import { useAccountStore } from "../../store/accountStore";
import { FlagBadge } from "../../components/ui/Badge";
import { fmtFecha } from "../../lib/fecha";

export default function DatosCuenta() {
  const cuenta = useAccountStore((s) => s.cuenta);

  if (!cuenta) {
    return <p className="text-sm text-[var(--color-ink-soft)]">Buscá una cuenta para ver sus datos.</p>;
  }

  const filas: Array<[string, string | number | null | React.ReactNode]> = [
    ["Nro de cuenta", cuenta.id_cta],
    ["Razón social", cuenta.razon_social_ent],
    ["Documento / Matrícula", cuenta.entidades_matricula_ent],
    ["Deuda actual", cuenta.deudaact_cta ? (
      <span className="font-bold text-[var(--color-danger)]">$ {Number(cuenta.deudaact_cta).toLocaleString("es-AR")}</span>
    ) : null],
    ["Deuda transferida", cuenta.deudatrans_cta ? (
      <span className="font-bold text-[var(--color-warning)]">$ {Number(cuenta.deudatrans_cta).toLocaleString("es-AR")}</span>
    ) : null],
    ["Fecha de ingreso", fmtFecha(cuenta.fechaingreso_cta)],
    ["Contacto", cuenta.entidad?.contacto_ent ?? null],
    ["Cliente", cuenta.cliente_desc],
    ["Subcliente", cuenta.subcliente_nombre],
    ["Estado", cuenta.estado_desc],
    ["Subestado", cuenta.sub_estado_desc],
    ["Empleador", cuenta.empleador_cta],
    ["Cuenta activa", <FlagBadge value={cuenta.activa_cta} labels={["Sí", "No"]} tones={["success", "neutral"]} />],
    ["Observación", cuenta.observacion_cta],
  ];

  return (
    <div className="space-y-6 animate-in">
      <div>
        <h2 className="section-title">
          <i className="fas fa-id-card" /> Datos de la cuenta
        </h2>
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3">
          {filas.map(([label, valor]) => (
            <div key={label}>
              <dt className="text-xs text-[var(--color-ink-soft)]">{label}</dt>
              <dd className="text-sm font-data">{valor ?? "—"}</dd>
            </div>
          ))}
        </dl>
      </div>

      {cuenta.telefonos.length > 0 && (
        <div>
          <h3 className="section-title">
            <i className="fas fa-phone" /> Teléfonos
          </h3>
          <div className="flex flex-wrap gap-2">
            {cuenta.telefonos.map((t, i) => (
              <span key={i} className="text-sm font-data bg-[var(--color-brand-soft)] rounded-md px-2 py-1">
                ({t.codigo_area_tel}) {t.numero_tel}
                {t.tipo_tel ? <span className="text-[var(--color-ink-soft)]"> · {t.tipo_tel}</span> : null}
              </span>
            ))}
          </div>
        </div>
      )}

      {cuenta.direcciones.length > 0 && (
        <div>
          <h3 className="section-title">
            <i className="fas fa-home" /> Domicilios
          </h3>
          <ul className="text-sm space-y-1">
            {cuenta.direcciones.map((d, i) => (
              <li key={i}>
                {d.calle_dir} {d.nro_dir}
                {d.barrio_dir ? `, ${d.barrio_dir}` : ""}
                {d.localidad_dir ? `, ${d.localidad_dir}` : ""}
                {d.provincia_dir ? `, ${d.provincia_dir}` : ""}
              </li>
            ))}
          </ul>
        </div>
      )}

      {cuenta.mails.length > 0 && (
        <div>
          <h3 className="section-title">
            <i className="fas fa-envelope" /> Mails
          </h3>
          <ul className="text-sm space-y-1">
            {cuenta.mails.map((m, i) => (
              <li key={i}>{m.mail}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
