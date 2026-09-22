import { useEffect, useState, useTransition } from "react";
import { api } from "../../api/client";
import { descargarExcel } from "../../api/download";
import { EmptyState } from "../../components/ui/EmptyState";
import { TableSkeleton } from "../../components/ui/Skeleton";
import { StatCard } from "../../components/ui/StatCard";
import { FlagBadge } from "../../components/ui/Badge";
import { toast } from "../../store/toastStore";
import { fmtFecha } from "../../lib/fecha";

interface SubEstadoOpt {
  id_sub_est: number;
  desc_sub_est: string;
}

interface FilaCuenta {
  id_cta: number;
  subestado: string | null;
  estado: string | null;
  matricula: string | null;
  razon_social: string | null;
  cuenta_cliente: string | null;
  cliente: string | null;
  subcliente: string | null;
  deuda_actual: string | null;
  deuda_transferida: string | null;
  fecha_ingreso: string | null;
  empleador: string | null;
  judicial: string | null;
  activa: string | null;
  observacion: string | null;
}

export default function InformeCuentas() {
  const [subestadoId, setSubestadoId] = useState("");
  const [subestados, setSubestados] = useState<SubEstadoOpt[]>([]);
  const [filas, setFilas] = useState<FilaCuenta[]>([]);
  const [loading, setLoading] = useState(false);
  const [exportando, setExportando] = useState(false);
  const [pending, startTransition] = useTransition();

  const qs = () => {
    const params = new URLSearchParams();
    if (subestadoId) params.set("subestado_id", subestadoId);
    return params.toString();
  };

  const cargar = () => {
    setLoading(true);
    api.get<{ filas: FilaCuenta[] }>(`/informes/cuentas?${qs()}`)
      .then((response) => startTransition(() => setFilas(response.data.filas)))
      .catch(() => toast.error("No se pudo cargar el informe."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
    api.get<SubEstadoOpt[]>("/catalogos/sub_estados")
      .then((response) => setSubestados(response.data))
      .catch(() => toast.error("No se pudieron cargar los subestados."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const exportar = async () => {
    setExportando(true);
    try {
      await descargarExcel(`/informes/cuentas/export?${qs()}`, "informe_cuentas.xlsx");
      toast.success("Informe exportado.");
    } catch {
      toast.error("No se pudo exportar el informe.");
    } finally {
      setExportando(false);
    }
  };

  const dinero = (valor: string | null) => valor ? `$ ${Number(valor).toLocaleString("es-AR")}` : "—";

  return (
    <div className="animate-in">
      <div className="flex items-center justify-between mb-4 gap-2 flex-wrap">
        <h2 className="section-title" style={{ ["--st-accent" as string]: "var(--color-info)" }}><i className="fas fa-file-invoice-dollar" /> Informe de Cuentas</h2>
        <button type="button" className="btn btn-success" onClick={exportar} disabled={exportando || !filas.length}>
          {exportando ? <><i className="fas fa-circle-notch fa-spin" /> Exportando...</> : <><i className="fas fa-file-excel" /> Exportar a Excel</>}
        </button>
      </div>

      <div className="flex gap-3 mb-4 items-end flex-wrap">
        <div>
          <label className="form-label">Subestado</label>
          <select value={subestadoId} onChange={(event) => setSubestadoId(event.target.value)} className="form-input">
            <option value="">Todos</option>
            {subestados.map((subestado) => (
              <option key={subestado.id_sub_est} value={subestado.id_sub_est}>{subestado.desc_sub_est}</option>
            ))}
          </select>
        </div>
        <button type="button" className="btn btn-secondary" onClick={cargar} disabled={loading}>
          <i className="fas fa-filter" /> Filtrar
        </button>
      </div>

      {!loading && filas.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4" style={{ opacity: pending ? 0.6 : 1 }}>
          <StatCard label="Cuentas" value={filas.length} icon="fa-file-invoice-dollar" tone="brand" />
          <StatCard label="Activas" value={filas.filter((fila) => fila.activa === "S").length} icon="fa-circle-check" tone="success" />
        </div>
      )}

      {loading ? <TableSkeleton rows={6} cols={10} /> : filas.length === 0 ? <EmptyState icon="fa-file-circle-xmark" title="Sin resultados" hint="Probá ajustar los filtros." /> : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]" style={{ opacity: pending ? 0.6 : 1, transition: "opacity 0.15s" }}>
          <table className="data-table">
            <thead><tr>
              <th>Cuenta</th><th>Subestado</th><th>Estado</th><th>Matrícula</th><th>Razón social</th>
              <th>Cuenta cliente</th><th>Cliente</th><th>Subcliente</th><th>Deuda actual</th><th>Deuda transferida</th><th>Ingreso</th><th>Activa</th>
            </tr></thead>
            <tbody>{filas.map((fila) => (
              <tr key={fila.id_cta}>
                <td className="font-data">{fila.id_cta}</td>
                <td>{fila.subestado ?? "—"}</td><td>{fila.estado ?? "—"}</td>
                <td className="font-data">{fila.matricula ?? "—"}</td><td>{fila.razon_social ?? "—"}</td><td className="font-data">{fila.cuenta_cliente ?? "—"}</td>
                <td>{fila.cliente ?? "—"}</td><td>{fila.subcliente ?? "—"}</td>
                <td className="font-data">{dinero(fila.deuda_actual)}</td><td className="font-data">{dinero(fila.deuda_transferida)}</td><td className="font-data">{fmtFecha(fila.fecha_ingreso)}</td>
                <td><FlagBadge value={fila.activa} labels={["Activa", "Inactiva"]} tones={["success", "neutral"]} /></td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}
    </div>
  );
}