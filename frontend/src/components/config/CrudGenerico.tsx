import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { toast } from "../../store/toastStore";
import { ConfirmDialog } from "../ui/ConfirmDialog";
import { Modal } from "../ui/Modal";
import { TableSkeleton } from "../ui/Skeleton";
import { EmptyState } from "../ui/EmptyState";

export interface ColumnaConfig {
  key: string;
  label: string;
  tipo?: "text" | "number" | "select";
  opciones?: { value: number | string; label: string }[];
  requerido?: boolean;
  /** Se muestra en la tabla pero no es editable (ej: PK autoincremental). */
  soloTabla?: boolean;
  /** Solo aparece en el form (ej: combo virtual que no existe como campo plano en la respuesta del backend). */
  soloForm?: boolean;
}

interface Props {
  titulo: string;
  icono: string;
  endpoint: string;
  /** Nombre(s) del/los campo(s) que forman la PK, en el orden que espera la URL del backend. */
  idFields: string[];
  columnas: ColumnaConfig[];
  campoActivo?: string;
  /** Transforma el form antes de POST/PATCH (ej: un combo que codifica 2 campos del backend en 1 select). */
  transformarEnvio?: (form: Record<string, string | number>) => Record<string, unknown>;
  /** Completa el form al editar con valores derivados del item (contraparte de transformarEnvio). */
  transformarEdicion?: (item: Record<string, unknown>) => Record<string, string | number>;
}

/** ABM genérico de catálogo: tabla + modal alta/edición, reusado por las entidades simples de Configuración. */
export default function CrudGenerico({
  titulo,
  icono,
  endpoint,
  idFields,
  columnas,
  campoActivo = "activo",
  transformarEnvio,
  transformarEdicion,
}: Props) {
  const [items, setItems] = useState<Record<string, unknown>[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState<Record<string, unknown> | null>(null);
  const [form, setForm] = useState<Record<string, string | number>>({});
  const [guardando, setGuardando] = useState(false);
  const [aDarBaja, setADarBaja] = useState<Record<string, unknown> | null>(null);

  const camposEditables = columnas.filter((c) => !c.soloTabla);
  const columnasTabla = columnas.filter((c) => !c.soloForm);

  const formVacio = () => Object.fromEntries(camposEditables.map((c) => [c.key, c.tipo === "number" ? 0 : ""]));

  const cargar = () => {
    setLoading(true);
    api
      .get<Record<string, unknown>[]>(endpoint)
      .then((r) => setItems(r.data))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  };

  useEffect(cargar, [endpoint]);

  const idsDe = (item: Record<string, unknown>) => idFields.map((f) => item[f]);
  const urlDetalle = (item: Record<string, unknown>) => `${endpoint}/${idsDe(item).join("/")}`;

  const abrirAlta = () => {
    setEditando(null);
    setForm(formVacio());
    setModalOpen(true);
  };

  const abrirEdicion = (item: Record<string, unknown>) => {
    setEditando(item);
    const f: Record<string, string | number> = {};
    camposEditables.forEach((c) => {
      f[c.key] = (item[c.key] as string | number) ?? (c.tipo === "number" ? 0 : "");
    });
    setForm({ ...f, ...transformarEdicion?.(item) });
    setModalOpen(true);
  };

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    setGuardando(true);
    try {
      const payload = transformarEnvio ? transformarEnvio(form) : form;
      if (editando == null) {
        await api.post(endpoint, payload);
        toast.success(`${titulo}: registro creado.`);
      } else {
        await api.patch(urlDetalle(editando), payload);
        toast.success(`${titulo}: registro actualizado.`);
      }
      setModalOpen(false);
      cargar();
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo guardar.");
    } finally {
      setGuardando(false);
    }
  };

  const confirmarBaja = async () => {
    if (!aDarBaja) return;
    try {
      await api.delete(urlDetalle(aDarBaja));
      toast.success(`${titulo}: registro dado de baja.`);
      cargar();
    } catch {
      toast.error("No se pudo dar de baja.");
    } finally {
      setADarBaja(null);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between gap-2 flex-wrap mb-3">
        <h3 className="section-title text-sm">
          <i className={`fas ${icono}`} /> {titulo}
        </h3>
        <button type="button" className="btn btn-secondary btn-sm" onClick={abrirAlta}>
          <i className="fas fa-plus" /> Nuevo
        </button>
      </div>

      {loading ? (
        <TableSkeleton rows={4} cols={columnasTabla.length + 1} />
      ) : items.length === 0 ? (
        <EmptyState icon="fa-table" title="Sin registros" hint="Todavía no hay nada cargado acá." />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
          <table className="data-table">
            <thead>
              <tr>
                {columnasTabla.map((c) => (
                  <th key={c.key}>{c.label}</th>
                ))}
                <th className="text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={idsDe(item).join("-")}>
                  {columnasTabla.map((c) => (
                    <td key={c.key}>
                      {c.tipo === "select"
                        ? c.opciones?.find((o) => o.value === item[c.key])?.label ?? String(item[c.key] ?? "—")
                        : String(item[c.key] ?? "—")}
                    </td>
                  ))}
                  <td className="text-right whitespace-nowrap">
                    <button type="button" className="btn btn-ghost btn-sm" onClick={() => abrirEdicion(item)}>
                      <i className="fas fa-pen" /> Editar
                    </button>
                    {item[campoActivo] !== "N" && (
                      <button type="button" className="btn btn-ghost-danger btn-sm" onClick={() => setADarBaja(item)}>
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
        title={editando == null ? `Nuevo (${titulo})` : `Editar (${titulo})`}
        icon={icono}
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" form="form-crud-generico" className="btn btn-success" disabled={guardando}>
              {guardando ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-crud-generico" onSubmit={guardar} className="space-y-3">
          {camposEditables.map((c) => (
            <div key={c.key}>
              <label className="form-label">{c.label}</label>
              {c.tipo === "select" ? (
                <select
                  value={form[c.key] ?? ""}
                  onChange={(e) => {
                    const opcion = c.opciones?.find((o) => String(o.value) === e.target.value);
                    setForm({ ...form, [c.key]: opcion ? opcion.value : e.target.value });
                  }}
                  className="form-input"
                  required={c.requerido}
                >
                  <option value="">Seleccionar...</option>
                  {c.opciones?.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={c.tipo === "number" ? "number" : "text"}
                  value={form[c.key] ?? ""}
                  onChange={(e) =>
                    setForm({ ...form, [c.key]: c.tipo === "number" ? Number(e.target.value) : e.target.value })
                  }
                  className="form-input"
                  required={c.requerido}
                />
              )}
            </div>
          ))}
        </form>
      </Modal>

      <ConfirmDialog
        open={aDarBaja != null}
        title="Dar de baja"
        message="¿Dar de baja este registro?"
        confirmLabel="Dar de baja"
        onConfirm={confirmarBaja}
        onCancel={() => setADarBaja(null)}
      />
    </div>
  );
}
