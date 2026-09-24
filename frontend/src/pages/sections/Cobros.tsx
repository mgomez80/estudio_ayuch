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
import type { CobroOut, ConceptoCobroOut } from "../../types/domain";
import { fmtFecha } from "../../lib/fecha";

const FORM_VACIO = { fcha_cobro: "", conceptos_id_concepto: 0, importe: "", rendido: "N" };

export default function Cobros() {
  const { idCta } = useParams();
  const [cobros, setCobros] = useState<CobroOut[]>([]);
  const [conceptos, setConceptos] = useState<ConceptoCobroOut[]>([]);
  const [loading, setLoading] = useState(true);

  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);

  const [aAnular, setAAnular] = useState<CobroOut | null>(null);

  const cargar = useCallback(() => {
    if (!idCta) return;
    setLoading(true);
    Promise.all([
      api.get<CobroOut[]>(`/cuentas/${idCta}/cobros`),
      api.get<ConceptoCobroOut[]>("/catalogos/conceptos-cobro"),
    ])
      .then(([cobrosRes, conceptosRes]) => {
        setCobros(cobrosRes.data);
        setConceptos(conceptosRes.data);
      })
      .catch(() => toast.error("No se pudieron cargar los cobros."))
      .finally(() => setLoading(false));
  }, [idCta]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const abrirAlta = () => {
    setForm({
      ...FORM_VACIO,
      fcha_cobro: new Date().toISOString().slice(0, 10),
      conceptos_id_concepto: conceptos[0]?.id_concepto ?? 0,
    });
    setModalOpen(true);
  };

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.fcha_cobro || !form.conceptos_id_concepto || !form.importe) return;
    setGuardando(true);
    try {
      await api.post(`/cuentas/${idCta}/cobros`, {
        fcha_cobro: form.fcha_cobro,
        conceptos_id_concepto: form.conceptos_id_concepto,
        importe: Number(form.importe),
        rendido: form.rendido,
      });
      toast.success("Cobro cargado.");
      setModalOpen(false);
      cargar();
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo cargar el cobro.");
    } finally {
      setGuardando(false);
    }
  };

  const confirmarAnular = async () => {
    if (!aAnular) return;
    try {
      await api.patch(`/cobros/${aAnular.id_cobros}/anular`);
      toast.success("Cobro anulado.");
      cargar();
    } catch {
      toast.error("No se pudo anular el cobro.");
    } finally {
      setAAnular(null);
    }
  };

  if (!idCta) return null;

  const vigentes = cobros.filter((c) => c.anulado !== "S");
  const totalCobrado = vigentes.reduce((acc, c) => acc + Number(c.importe || 0), 0);
  const totalRendido = vigentes.filter((c) => c.rendido === "S").reduce((acc, c) => acc + Number(c.importe || 0), 0);
  const dinero = (v: number) => `$ ${v.toLocaleString("es-AR", { minimumFractionDigits: 2 })}`;

  return (
    <div className="animate-in">
      <div className="flex items-center justify-between gap-2 flex-wrap mb-4">
        <h2 className="section-title">
          <i className="fas fa-hand-holding-dollar" /> Cobros
        </h2>
        <button type="button" className="btn btn-secondary" onClick={abrirAlta}>
          <i className="fas fa-plus" /> Nuevo cobro
        </button>
      </div>

      {!loading && cobros.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
          <StatCard label="Cobrado (vigente)" value={dinero(totalCobrado)} icon="fa-sack-dollar" tone="brand" />
          <StatCard label="Rendido" value={dinero(totalRendido)} icon="fa-circle-check" tone="success" />
          <StatCard label="Pendiente de rendir" value={dinero(totalCobrado - totalRendido)} icon="fa-clock" tone="neutral" />
        </div>
      )}

      {loading ? (
        <TableSkeleton rows={5} cols={6} />
      ) : cobros.length === 0 ? (
        <EmptyState icon="fa-hand-holding-dollar" title="Sin cobros" hint="Registrá el primer cobro para esta cuenta." />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
          <table className="data-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Concepto</th>
                <th>Importe</th>
                <th>Rendido</th>
                <th>Estado</th>
                <th className="text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {cobros.map((c) => (
                <tr key={c.id_cobros}>
                  <td className="font-data">{fmtFecha(c.fcha_cobro)}</td>
                  <td>{c.concepto ?? "—"}</td>
                  <td className="font-data">{dinero(Number(c.importe || 0))}</td>
                  <td><FlagBadge value={c.rendido} labels={["Sí", "No"]} tones={["success", "warning"]} /></td>
                  <td><FlagBadge value={c.anulado === "S" ? "N" : "S"} labels={["Vigente", "Anulado"]} tones={["success", "danger"]} /></td>
                  <td className="text-right whitespace-nowrap">
                    {c.anulado !== "S" && (
                      <button type="button" className="btn btn-ghost-danger btn-sm" onClick={() => setAAnular(c)}>
                        <i className="fas fa-ban" /> Anular
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
        title="Nuevo cobro"
        icon="fa-hand-holding-dollar"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>Cancelar</button>
            <button type="submit" form="form-cobro" className="btn btn-success" disabled={guardando}>
              {guardando ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-cobro" onSubmit={guardar} className="space-y-3">
          <div>
            <label className="form-label">Fecha</label>
            <input
              type="date"
              value={form.fcha_cobro}
              onChange={(e) => setForm({ ...form, fcha_cobro: e.target.value })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Concepto</label>
            <select
              value={form.conceptos_id_concepto}
              onChange={(e) => setForm({ ...form, conceptos_id_concepto: Number(e.target.value) })}
              className="form-input"
              required
            >
              <option value={0}>Seleccionar...</option>
              {conceptos.map((c) => (
                <option key={c.id_concepto} value={c.id_concepto}>{c.desc_concepto}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="form-label">Monto</label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={form.importe}
              onChange={(e) => setForm({ ...form, importe: e.target.value })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Rendido</label>
            <select
              value={form.rendido}
              onChange={(e) => setForm({ ...form, rendido: e.target.value })}
              className="form-input"
            >
              <option value="N">No</option>
              <option value="S">Sí</option>
            </select>
          </div>
        </form>
      </Modal>

      <ConfirmDialog
        open={aAnular != null}
        title="Anular cobro"
        message="¿Anular este cobro? Queda registrado como anulado, no se borra."
        confirmLabel="Anular"
        onConfirm={confirmarAnular}
        onCancel={() => setAAnular(null)}
      />
    </div>
  );
}
