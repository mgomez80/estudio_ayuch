import { useEffect, useState, useTransition } from "react";
import { api } from "../../api/client";
import { descargarExcel } from "../../api/download";
import { FlagBadge } from "../../components/ui/Badge";
import { TableSkeleton } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { StatCard } from "../../components/ui/StatCard";
import { toast } from "../../store/toastStore";

interface ClienteOpt {
  id_cliente: number;
  cuenta_cliente: number;
  desc_cliente: string;
}

interface SubclienteOpt {
  id_subcli: number;
  nombre_subcli: string;
}

interface FilaTelefono {
  id_cta: number | null;
  cliente: string | null;
  subcliente: string | null;
  razon_social: string | null;
  tipo: string | null;
  cod_area: string | null;
  numero: string | null;
  activo: string | null;
}

export default function InformeTelefonos() {
  const [activo, setActivo] = useState("");
  const [tipo, setTipo] = useState("");
  const [clienteId, setClienteId] = useState("");
  const [subclienteId, setSubclienteId] = useState("");
  const [tipos, setTipos] = useState<string[]>([]);
  const [clientes, setClientes] = useState<ClienteOpt[]>([]);
  const [subclientes, setSubclientes] = useState<SubclienteOpt[]>([]);
  const [filas, setFilas] = useState<FilaTelefono[]>([]);
  const [loading, setLoading] = useState(false);
  const [exportando, setExportando] = useState(false);
  const [pending, startTransition] = useTransition();

  const qs = () => {
    const p = new URLSearchParams();
    if (activo) p.set("activo", activo);
    if (tipo) p.set("tipo", tipo);
    if (clienteId) p.set("cliente_id", clienteId);
    if (subclienteId) p.set("subcliente_id", subclienteId);
    return p.toString();
  };

  const cargar = () => {
    setLoading(true);
    api
      .get<{ filas: FilaTelefono[] }>(`/informes/telefonos?${qs()}`)
      .then((r) => {
        startTransition(() => {
          setFilas(r.data.filas);
        });
      })
      .catch(() => toast.error("No se pudo cargar el informe."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
    Promise.all([
      api.get<string[]>("/informes/telefonos/tipos"),
      api.get<ClienteOpt[]>("/catalogos/clientes"),
      api.get<SubclienteOpt[]>("/catalogos/subclientes"),
    ])
      .then(([t, c, s]) => {
        setTipos(t.data);
        setClientes(c.data);
        setSubclientes(s.data);
      })
      .catch(() => toast.error("No se pudieron cargar los catálogos de filtros."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const exportar = async () => {
    setExportando(true);
    try {
      await descargarExcel(`/informes/telefonos/export?${qs()}`, "informe_telefonos.xlsx");
      toast.success("Informe exportado.");
    } catch {
      toast.error("No se pudo exportar el informe.");
    } finally {
      setExportando(false);
    }
  };

  return (
    <div className="animate-in">
      <div className="flex items-center justify-between mb-4 gap-2 flex-wrap">
        <h2 className="section-title" style={{ ["--st-accent" as string]: "var(--color-info)" }}><i className="fas fa-phone" /> Informe de Teléfonos</h2>
        <button type="button" className="btn btn-success" onClick={exportar} disabled={exportando || !filas.length}>
          {exportando ? <><i className="fas fa-circle-notch fa-spin" /> Exportando...</> : <><i className="fas fa-file-excel" /> Exportar a Excel</>}
        </button>
      </div>

      <div className="flex gap-3 mb-4 items-end flex-wrap">
        <div>
          <label className="form-label">Activo</label>
          <select value={activo} onChange={(e) => setActivo(e.target.value)} className="form-select">
            <option value="">Todos</option>
            <option value="S">Sí</option>
            <option value="N">No</option>
          </select>
        </div>
        <div>
          <label className="form-label">Tipo</label>
          <select value={tipo} onChange={(e) => setTipo(e.target.value)} className="form-select">
            <option value="">Todos</option>
            {tipos.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="form-label">Cliente</label>
          <select value={clienteId} onChange={(e) => setClienteId(e.target.value)} className="form-select">
            <option value="">Todos</option>
            {clientes.map((c) => (
              <option key={`${c.id_cliente}-${c.cuenta_cliente}`} value={c.id_cliente}>
                {c.desc_cliente}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="form-label">Subcliente</label>
          <select value={subclienteId} onChange={(e) => setSubclienteId(e.target.value)} className="form-select">
            <option value="">Todos</option>
            {subclientes.map((s) => (
              <option key={s.id_subcli} value={s.id_subcli}>{s.nombre_subcli}</option>
            ))}
          </select>
        </div>
        <button type="button" className="btn btn-secondary" onClick={cargar} disabled={loading}>
          <i className="fas fa-filter" /> Filtrar
        </button>
      </div>

      {!loading && filas.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4" style={{ opacity: pending ? 0.6 : 1 }}>
          <StatCard label="Teléfonos" value={filas.length} icon="fa-phone" tone="brand" />
          <StatCard label="Activos" value={filas.filter((f) => f.activo === "S").length} icon="fa-circle-check" tone="success" />
        </div>
      )}

      {loading ? (
        <TableSkeleton rows={6} cols={8} />
      ) : filas.length === 0 ? (
        <EmptyState icon="fa-file-circle-xmark" title="Sin resultados" hint="Probá ajustar los filtros." />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]" style={{ opacity: pending ? 0.6 : 1, transition: "opacity 0.15s" }}>
          <table className="data-table">
            <thead>
              <tr className="text-left text-xs text-[var(--color-ink-soft)] border-b border-[var(--color-line)]">
                <th className="py-1.5">Cuenta</th>
                <th>Cliente</th>
                <th>Subcliente</th>
                <th>Razón social</th>
                <th>Tipo</th>
                <th>Código área</th>
                <th>Número</th>
                <th>Activo</th>
              </tr>
            </thead>
            <tbody>
              {filas.map((f, i) => (
                <tr key={i} className="border-b border-[var(--color-line)]">
                  <td className="py-1.5 font-data">{f.id_cta ?? "—"}</td>
                  <td>{f.cliente ?? "—"}</td>
                  <td>{f.subcliente ?? "—"}</td>
                  <td>{f.razon_social ?? "—"}</td>
                  <td>{f.tipo ?? "—"}</td>
                  <td className="font-data">{f.cod_area ?? "—"}</td>
                  <td className="font-data">{f.numero ?? "—"}</td>
                  <td><FlagBadge value={f.activo} labels={["Activo","Inactivo"]} tones={["success","neutral"]} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
