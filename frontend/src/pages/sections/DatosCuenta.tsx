import { useState } from "react";
import { useAccountStore } from "../../store/accountStore";
import { FlagBadge } from "../../components/ui/Badge";
import { Modal } from "../../components/ui/Modal";
import { toast } from "../../store/toastStore";
import { api } from "../../api/client";
import { fmtFecha } from "../../lib/fecha";
import type { CuentaDetalleOut } from "../../types/domain";

function mensajeError(err: unknown, fallback: string): string {
  const detail = (err as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(" / ") || fallback;
  }
  return fallback;
}

export default function DatosCuenta() {
  const cuenta = useAccountStore((s) => s.cuenta);
  const setCuenta = useAccountStore((s) => s.setCuenta);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState({
    matricula: "", razon_social: "", deudaact_cta: "", deudatrans_cta: "",
    empleador_cta: "", cuenta_cliente: "", observacion_cta: "",
  });
  const [guardando, setGuardando] = useState(false);

  if (!cuenta) {
    return <p className="text-sm text-[var(--color-ink-soft)]">Buscá una cuenta para ver sus datos.</p>;
  }

  const abrirEdicion = () => {
    setForm({
      matricula: cuenta.entidades_matricula_ent,
      razon_social: cuenta.razon_social_ent ?? "",
      deudaact_cta: cuenta.deudaact_cta ?? "",
      deudatrans_cta: cuenta.deudatrans_cta ?? "",
      empleador_cta: cuenta.empleador_cta ?? "",
      cuenta_cliente: cuenta.cuenta_cliente ?? "",
      observacion_cta: cuenta.observacion_cta ?? "",
    });
    setModalOpen(true);
  };

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    setGuardando(true);
    try {
      const { data } = await api.patch<CuentaDetalleOut>(`/cuentas/${cuenta.id_cta}`, {
        matricula: form.matricula,
        razon_social: form.razon_social,
        deudaact_cta: form.deudaact_cta === "" ? null : Number(form.deudaact_cta),
        deudatrans_cta: form.deudatrans_cta === "" ? null : Number(form.deudatrans_cta),
        empleador_cta: form.empleador_cta || null,
        cuenta_cliente: form.cuenta_cliente || null,
        observacion_cta: form.observacion_cta || null,
      });
      setCuenta(data);
      toast.success("Cuenta actualizada.");
      setModalOpen(false);
    } catch (err) {
      toast.error(mensajeError(err, "No se pudo actualizar la cuenta."));
    } finally {
      setGuardando(false);
    }
  };

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
        <div className="flex items-center justify-between gap-2 flex-wrap mb-2">
          <h2 className="section-title">
            <i className="fas fa-id-card" /> Datos de la cuenta
          </h2>
          <button type="button" className="btn btn-secondary btn-sm" onClick={abrirEdicion}>
            <i className="fas fa-pen" /> Editar cuenta
          </button>
        </div>
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

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Editar cuenta"
        icon="fa-pen"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button type="submit" form="form-editar-cuenta" className="btn btn-success" disabled={guardando}>
              {guardando ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-editar-cuenta" onSubmit={guardar} className="space-y-3">
          <div>
            <label className="form-label">Documento / Matrícula</label>
            <input
              type="text"
              value={form.matricula}
              onChange={(e) => setForm({ ...form, matricula: e.target.value })}
              className="form-input"
              required
              autoFocus
            />
          </div>
          <div>
            <label className="form-label">Razón social</label>
            <input
              type="text"
              value={form.razon_social}
              onChange={(e) => setForm({ ...form, razon_social: e.target.value })}
              className="form-input"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="form-label">Deuda actual</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={form.deudaact_cta}
                onChange={(e) => setForm({ ...form, deudaact_cta: e.target.value })}
                className="form-input"
              />
            </div>
            <div>
              <label className="form-label">Deuda transferida</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={form.deudatrans_cta}
                onChange={(e) => setForm({ ...form, deudatrans_cta: e.target.value })}
                className="form-input"
              />
            </div>
          </div>
          <div>
            <label className="form-label">Empleador</label>
            <input
              type="text"
              value={form.empleador_cta}
              onChange={(e) => setForm({ ...form, empleador_cta: e.target.value })}
              className="form-input"
            />
          </div>
          <div>
            <label className="form-label">N° cuenta cliente</label>
            <input
              type="text"
              value={form.cuenta_cliente}
              onChange={(e) => setForm({ ...form, cuenta_cliente: e.target.value })}
              className="form-input"
            />
          </div>
          <div>
            <label className="form-label">Observación</label>
            <textarea
              value={form.observacion_cta}
              onChange={(e) => setForm({ ...form, observacion_cta: e.target.value })}
              className="form-input"
              rows={2}
            />
          </div>
        </form>
      </Modal>
    </div>
  );
}
