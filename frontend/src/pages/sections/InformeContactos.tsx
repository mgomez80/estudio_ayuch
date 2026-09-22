import { useEffect, useState, useTransition } from "react";
import { api } from "../../api/client";
import { descargarExcel } from "../../api/download";
import { EmptyState } from "../../components/ui/EmptyState";
import { TableSkeleton } from "../../components/ui/Skeleton";
import { StatCard } from "../../components/ui/StatCard";
import { toast } from "../../store/toastStore";
import { fmtFecha } from "../../lib/fecha";

interface UsuarioCat {
  id_usuario: number;
  nombre: string;
}

interface SubEstadoOpt {
  id_sub_est: number;
  desc_sub_est: string;
}

interface FilaContacto {
  id_cta: number;
  subestado: string | null;
  matricula: string | null;
  razon_social: string | null;
  fecha: string | null;
  hora: string | null;
  nota: string | null;
  usuario: string | null;
}

export default function InformeContactos() {
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [usuarioId, setUsuarioId] = useState("");
  const [subestadoId, setSubestadoId] = useState("");
  const [usuarios, setUsuarios] = useState<UsuarioCat[]>([]);
  const [subestados, setSubestados] = useState<SubEstadoOpt[]>([]);
  const [filas, setFilas] = useState<FilaContacto[]>([]);
  const [loading, setLoading] = useState(false);
  const [exportando, setExportando] = useState(false);
  const [pending, startTransition] = useTransition();

  const qs = () => {
    const p = new URLSearchParams();
    if (desde) p.set("desde", desde);
    if (hasta) p.set("hasta", hasta);
    if (usuarioId) p.set("usuario_id", usuarioId);
    if (subestadoId) p.set("subestado_id", subestadoId);
    return p.toString();
  };

  const cargar = () => {
    setLoading(true);
    api
      .get<{ filas: FilaContacto[] }>(`/informes/contactos?${qs()}`)
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
      api.get<UsuarioCat[]>("/catalogos/ejecutivos"),
      api.get<SubEstadoOpt[]>("/catalogos/sub_estados"),
    ])
      .then(([u, s]) => {
        setUsuarios(u.data);
        setSubestados(s.data);
      })
      .catch(() => toast.error("No se pudieron cargar los catálogos de filtros."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const exportar = async () => {
    setExportando(true);
    try {
      await descargarExcel(`/informes/contactos/export?${qs()}`, "informe_contactos.xlsx");
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
        <h2 className="section-title" style={{ ["--st-accent" as string]: "var(--color-info)" }}><i className="fas fa-phone" /> Informe de Contactos</h2>
        <button type="button" className="btn btn-success" onClick={exportar} disabled={exportando || !filas.length}>
          {exportando ? <><i className="fas fa-circle-notch fa-spin" /> Exportando...</> : <><i className="fas fa-file-excel" /> Exportar a Excel</>}
        </button>
      </div>

      <div className="flex gap-3 mb-4 items-end flex-wrap">
        <div>
          <label className="form-label">Desde</label>
          <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} className="form-input" />
        </div>
        <div>
          <label className="form-label">Hasta</label>
          <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} className="form-input" />
        </div>
        <div>
          <label className="form-label">Usuario</label>
          <select value={usuarioId} onChange={(e) => setUsuarioId(e.target.value)} className="form-input">
            <option value="">Todos</option>
            {usuarios.map((u) => (
              <option key={u.id_usuario} value={u.id_usuario}>{u.nombre}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="form-label">Subestado</label>
          <select value={subestadoId} onChange={(e) => setSubestadoId(e.target.value)} className="form-input">
            <option value="">Todos</option>
            {subestados.map((s) => (
              <option key={s.id_sub_est} value={s.id_sub_est}>{s.desc_sub_est}</option>
            ))}
          </select>
        </div>
        <button type="button" className="btn btn-secondary" onClick={cargar} disabled={loading}>
          <i className="fas fa-filter" /> Filtrar
        </button>
      </div>

      {!loading && filas.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4" style={{ opacity: pending ? 0.6 : 1 }}>
          <StatCard label="Contactos" value={filas.length} icon="fa-comments" tone="brand" />
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
              <tr>
                <th>Cuenta</th>
                <th>Subestado</th>
                <th>Matrícula</th>
                <th>Razón social</th>
                <th>Fecha</th>
                <th>Hora</th>
                <th>Nota</th>
                <th>Usuario</th>
              </tr>
            </thead>
            <tbody>
              {filas.map((f, i) => (
                <tr key={i}>
                  <td className="font-data">{f.id_cta}</td>
                  <td>{f.subestado ?? "—"}</td>
                  <td className="font-data">{f.matricula ?? "—"}</td>
                  <td>{f.razon_social ?? "—"}</td>
                  <td className="font-data">{fmtFecha(f.fecha)}</td>
                  <td className="font-data">{f.hora ?? "—"}</td>
                  <td>{f.nota ?? "—"}</td>
                  <td>{f.usuario ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
