import { useAccountStore } from "../store/accountStore";

export default function CuentaHeader() {
  const cuenta = useAccountStore((s) => s.cuenta);
  if (!cuenta) return null;

  const esJudicial = cuenta.judicial === "S";
  const inactiva = cuenta.activa_cta === "N";

  const Dato = ({ label, children }: { label: string; children: React.ReactNode }) => (
    <div className="flex flex-col">
      <span className="text-[10px] uppercase tracking-wide text-[var(--color-ink-soft)] font-semibold">{label}</span>
      <span className="text-sm">{children}</span>
    </div>
  );

  return (
    <div className="space-y-2 animate-in">
      {inactiva && (
        <div className="badge badge-danger w-full justify-center py-2 text-sm rounded-lg">
          <i className="fas fa-ban" /> CUENTA INACTIVA
        </div>
      )}
      {esJudicial && (
        <div className="badge badge-judicial w-full justify-center py-2 text-sm rounded-lg">
          <i className="fas fa-gavel" /> ESTA ES UNA CUENTA JUDICIAL
        </div>
      )}

      <div
        className="card px-5 py-3.5 flex flex-wrap items-center gap-x-8 gap-y-2 relative overflow-hidden"
        style={{
          backgroundImage: esJudicial
            ? "linear-gradient(120deg, color-mix(in srgb, var(--color-judicial) 9%, var(--color-surface)), var(--color-surface) 55%)"
            : "linear-gradient(120deg, color-mix(in srgb, var(--color-brand) 8%, var(--color-surface)), var(--color-surface) 55%)",
        }}
      >
        <span
          className="absolute left-0 top-0 bottom-0 w-1.5"
          style={{
            backgroundImage: esJudicial
              ? "linear-gradient(180deg, #59359A, var(--color-judicial))"
              : "linear-gradient(180deg, var(--color-brand), var(--color-brand-accent))",
          }}
        />
        <Dato label={esJudicial ? "Cta Judicial" : "Cuenta"}>
          <span className="font-data font-semibold">{cuenta.id_cta}</span>
        </Dato>
        <Dato label="Documento">
          <span className="font-data">{cuenta.entidades_matricula_ent}</span>
        </Dato>
        <Dato label="Deudor">{cuenta.razon_social_ent ?? "—"}</Dato>
        <Dato label="Subestado">{cuenta.sub_estado_desc ?? cuenta.estado_desc ?? "—"}</Dato>
        <Dato label="Deuda con">
          {cuenta.cliente_desc ?? "—"}
          {cuenta.subcliente_nombre ? ` · ${cuenta.subcliente_nombre}` : ""}
        </Dato>
        <div className="ml-auto">
          <span className={`badge ${esJudicial ? "badge-judicial" : "badge-brand"}`}>
            {esJudicial ? "Judicial" : "Extrajudicial"}
          </span>
        </div>
      </div>
    </div>
  );
}
