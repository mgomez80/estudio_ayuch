import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../api/client";
import { FlagBadge } from "../../components/ui/Badge";
import { TableSkeleton } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { Modal } from "../../components/ui/Modal";
import { ConfirmDialog } from "../../components/ui/ConfirmDialog";
import { StatCard } from "../../components/ui/StatCard";
import { toast } from "../../store/toastStore";
import { useAccountStore } from "../../store/accountStore";
import type { ContactoOut, SubEstadoOut } from "../../types/domain";
import { fmtFecha } from "../../lib/fecha";

const FORM_VACIO = { fecha_contacto: "", hora_contacto: "", nota: "", sub_estados_id_sub_est: 0 };

export default function Contactos() {
  const { idCta } = useParams();
  const cuenta = useAccountStore((s) => s.cuenta);
  const setCuenta = useAccountStore((s) => s.setCuenta);
  const [contactos, setContactos] = useState<ContactoOut[]>([]);
  const [subEstados, setSubEstados] = useState<SubEstadoOut[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal ABM
  const [modalOpen, setModalOpen] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);
  const [form, setForm] = useState(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);

  // Confirmación de baja
  const [aDarBaja, setABaja] = useState<ContactoOut | null>(null);

  const cargar = useCallback(() => {
    if (!idCta) return;
    setLoading(true);
    Promise.all([
      api.get<ContactoOut[]>(`/cuentas/${idCta}/contactos`),
      api.get<SubEstadoOut[]>("/catalogos/sub_estados"),
    ])
      .then(([contactosRes, subEstadosRes]) => {
        setContactos(contactosRes.data);
        setSubEstados(subEstadosRes.data);
      })
      .finally(() => setLoading(false));
  }, [idCta]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const abrirAlta = () => {
    setEditId(null);
    setForm({ ...FORM_VACIO, sub_estados_id_sub_est: cuenta?.sub_estados_id_sub_est ?? 0 });
    setModalOpen(true);
  };

  const abrirEdicion = (item: ContactoOut) => {
    setEditId(item.id_contacto);
    setForm({
      fecha_contacto: item.fecha_contacto ?? "",
      hora_contacto: item.hora_contacto ?? "",
      nota: item.nota_contacto ?? "",
      sub_estados_id_sub_est: cuenta?.sub_estados_id_sub_est ?? 0,
    });
    setModalOpen(true);
  };

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.fecha_contacto || !form.hora_contacto) return;
    setGuardando(true);
    try {
      const payload = {
        fecha_contacto: form.fecha_contacto,
        hora_contacto: form.hora_contacto,
        nota: form.nota || null,
      };
      if (editId == null) {
        await api.post(`/cuentas/${idCta}/contactos`, payload);
        toast.success("Contacto creado.");
      } else {
        await api.patch(`/contactos/${editId}`, payload);
        toast.success("Contacto actualizado.");
      }
      if (form.sub_estados_id_sub_est && form.sub_estados_id_sub_est !== cuenta?.sub_estados_id_sub_est) {
        await api.patch(`/cuentas/${idCta}/sub-estado`, { id_sub_est: form.sub_estados_id_sub_est });
        if (cuenta) {
          const subEstado = subEstados.find((s) => s.id_sub_est === form.sub_estados_id_sub_est);
          setCuenta({ ...cuenta, sub_estados_id_sub_est: form.sub_estados_id_sub_est, sub_estado_desc: subEstado?.desc_sub_est ?? cuenta.sub_estado_desc });
        }
      }
      setModalOpen(false);
      cargar();
    } catch {
      toast.error("No se pudo guardar el contacto.");
    } finally {
      setGuardando(false);
    }
  };

  const confirmarBaja = async () => {
    if (!aDarBaja) return;
    try {
      await api.patch(`/contactos/${aDarBaja.id_contacto}/baja`);
      toast.success("Contacto dado de baja.");
      cargar();
    } catch {
      toast.error("No se pudo dar de baja el contacto.");
    } finally {
      setABaja(null);
    }
  };

  if (!idCta) return null;

  const activos = contactos.filter((c) => c.activo === "S").length;

  return (
    <div className="animate-in">
      <div className="flex items-center justify-between gap-2 flex-wrap mb-4">
        <h2 className="section-title">
          <i className="fas fa-address-book" /> Historial de contactos
        </h2>
        <button type="button" className="btn btn-secondary" onClick={abrirAlta}>
          <i className="fas fa-plus" /> Nuevo contacto
        </button>
      </div>

      {!loading && contactos.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
          <StatCard label="Contactos totales" value={contactos.length} icon="fa-address-book" tone="brand" />
          <StatCard label="Activos" value={activos} icon="fa-circle-check" tone="success" />
          <StatCard label="Dados de baja" value={contactos.length - activos} icon="fa-circle-minus" tone="neutral" />
        </div>
      )}

      {loading ? (
        <TableSkeleton rows={5} cols={6} />
      ) : contactos.length === 0 ? (
        <EmptyState
          icon="fa-address-book-plus"
          title="Sin contactos"
          hint="Registrá el primer contacto para esta cuenta."
        />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
          <table className="data-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Hora</th>
                <th>Usuario</th>
                <th>Nota</th>
                <th>Estado</th>
                <th className="text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {contactos.map((c) => (
                <tr key={c.id_contacto}>
                  <td className="font-data">{fmtFecha(c.fecha_contacto)}</td>
                  <td className="font-data">{c.hora_contacto ?? "—"}</td>
                  <td>{c.usuario_nombre ?? "—"}</td>
                  <td>{c.nota_contacto ?? "—"}</td>
                  <td><FlagBadge value={c.activo} labels={["Activo", "De baja"]} tones={["success", "neutral"]} /></td>
                  <td className="text-right whitespace-nowrap">
                    <button type="button" className="btn btn-ghost btn-sm" onClick={() => abrirEdicion(c)}>
                      <i className="fas fa-pen" /> Editar
                    </button>
                    {c.activo === "S" && (
                      <button type="button" className="btn btn-ghost-danger btn-sm" onClick={() => setABaja(c)}>
                        <i className="fas fa-ban" /> Baja
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editId == null ? "Nuevo contacto" : "Editar contacto"}
        icon="fa-address-book"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button type="submit" form="form-contacto" className="btn btn-success" disabled={guardando}>
              {guardando ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-contacto" onSubmit={guardar} className="space-y-3">
          <div>
            <label className="form-label">Fecha</label>
            <input
              type="date"
              value={form.fecha_contacto}
              onChange={(e) => setForm({ ...form, fecha_contacto: e.target.value })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Hora</label>
            <input
              type="time"
              value={form.hora_contacto}
              onChange={(e) => setForm({ ...form, hora_contacto: e.target.value })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Subestado</label>
            <select
              value={form.sub_estados_id_sub_est}
              onChange={(e) => setForm({ ...form, sub_estados_id_sub_est: Number(e.target.value) })}
              className="form-input"
            >
              <option value={0}>Seleccionar subestado...</option>
              {subEstados.map((s) => (
                <option key={s.id_sub_est} value={s.id_sub_est}>{s.desc_sub_est}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="form-label">Nota</label>
            <textarea
              value={form.nota}
              onChange={(e) => setForm({ ...form, nota: e.target.value })}
              className="form-input"
              rows={3}
            />
          </div>
        </form>
      </Modal>

      <ConfirmDialog
        open={aDarBaja != null}
        title="Dar de baja"
        message="¿Dar de baja este contacto?"
        confirmLabel="Dar de baja"
        onConfirm={confirmarBaja}
        onCancel={() => setABaja(null)}
      />
    </div>
  );
}
