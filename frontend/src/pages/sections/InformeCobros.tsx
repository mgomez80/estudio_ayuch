import { useEffect, useState, useTransition } from "react";
import { api } from "../../api/client";
import { descargarExcel } from "../../api/download";
import { EmptyState } from "../../components/ui/EmptyState";
import { TableSkeleton } from "../../components/ui/Skeleton";
import { StatCard } from "../../components/ui/StatCard";
import { FlagBadge } from "../../components/ui/Badge";
import { toast } from "../../store/toastStore";
import { fmtFecha } from "../../lib/fecha";
import type { FilaInformeCobro, ConceptoCobroOut } from "../../types/domain";

export default function InformeCobros() {
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [rendido, setRendido] = useState("");
  const [conceptoId, setConceptoId] = useState("");
  const [conceptos, setConceptos] = useState<ConceptoCobroOut[]>([]);
  const [filas, setFilas] = useState<FilaInformeCobro[]>([]);
  const [loading, setLoading] = useState(false);
  const [exportando, setExportando] = useState(false);
  const [pending, startTransition] = useTransition();

  const qs = () => {
    const params = new URLSearchParams();
    if (desde) params.set("desde", desde);
    if (hasta) params.set("hasta", hasta);
    if (rendido) params.set("rendido", rendido);
    if (conceptoId) params.set("concepto_id", conceptoId);
    return params.toString();
  };

  const cargar = () => {
    setLoading(true);
    api
      .get<{ filas: FilaInformeCobro[] }>(`/informes/cobros?${qs()}`)
      .then((response) => startTransition(() => setFilas(response.data.filas)))
      .catch(() => toast.error("No se pudo cargar el informe."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar();
    api.get<ConceptoCobroOut[]>("/catalogos/conceptos-cobro")
      .then((response) => setConceptos(response.data))
      .catch(() => undefined);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const exportar = async () => {
    setExportando(true);
    try {
      await descargarExcel(`/informes/cobros/export?${qs()}`, "informe_cobros.xlsx");
      toast.success("Informe exportado.");
    } catch {
      toast.error("No se pudo exportar el informe.");
    } finally {
      setExportando(false);
    }
  };

  const dinero = (valor: string | null) => (valor ? `$ ${Number(valor).toLocaleString("es-AR")}` : "—");
  const total = filas.reduce((acc, f) => acc + Number(f.importe || 0), 0);

  return (
    <div className="animate-in">
      <div className="flex items-center justify-between mb-4 gap-2 flex-wrap">
        <h2 className="section-title" style={{ ["--st-accent" as string]: "var(--color-info)" }}>
          <i className="fas fa-file-invoice-dollar" /> Informe de Cobros
        </h2>
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
          <label className="form-label">Rendido</label>
          <select value={rendido} onChange={(e) => setRendido(e.target.value)} className="form-input">
            <option value="">Todos</option>
            <option value="S">Sí</option>
            <option value="N">No</option>
          </select>
        </div>
        <div>
          <label className="form-label">Concepto</label>
          <select value={conceptoId} onChange={(e) => setConceptoId(e.target.value)} className="form-input">
            <option value="">Todos</option>
            {conceptos.map((c) => (
              <option key={c.id_concepto} value={c.id_concepto}>{c.desc_concepto}</option>
            ))}
          </select>
        </div>
        <button type="button" className="btn btn-secondary" onClick={cargar} disabled={loading}>
          <i className="fas fa-filter" /> Filtrar
        </button>
      </div>

      {!loading && filas.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4" style={{ opacity: pending ? 0.6 : 1 }}>
          <StatCard label="Cobros" value={filas.length} icon="fa-file-invoice-dollar" tone="brand" />
          <StatCard label="Total" value={`$ ${total.toLocaleString("es-AR")}`} icon="fa-sack-dollar" tone="success" />
        </div>
      )}

      {loading ? (
        <TableSkeleton rows={6} cols={7} />
      ) : filas.length === 0 ? (
        <EmptyState icon="fa-file-circle-xmark" title="Sin resultados" hint="Probá ajustar los filtros." />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]" style={{ opacity: pending ? 0.6 : 1, transition: "opacity 0.15s" }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Cuenta</th>
                <th>Matrícula</th>
                <th>Nombre de la cuenta</th>
                <th>Concepto</th>
                <th>Importe</th>
                <th>Rendido</th>
              </tr>
            </thead>
            <tbody>
              {filas.map((f) => (
                <tr key={f.id_cobros}>
                  <td className="font-data">{fmtFecha(f.fecha)}</td>
                  <td className="font-data">{f.id_cta}</td>
                  <td className="font-data">{f.matricula ?? "—"}</td>
                  <td>{f.razon_social ?? "—"}</td>
                  <td>{f.concepto ?? "—"}</td>
                  <td className="font-data">{dinero(f.importe)}</td>
                  <td><FlagBadge value={f.rendido} labels={["Sí", "No"]} tones={["success", "warning"]} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
