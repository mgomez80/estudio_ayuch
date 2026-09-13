import { useEffect, useRef, useState } from "react";
import { api } from "../../api/client";
import { toast } from "../../store/toastStore";
import type { SubEstadoOut, EjecutivoOut, CambioMasivoResult } from "../../types/domain";

type Accion = "reasignacion" | "sub-estado";

export default function CambiosMasivosTab() {
  const [accion, setAccion] = useState<Accion>("reasignacion");
  const [ejecutivos, setEjecutivos] = useState<EjecutivoOut[]>([]);
  const [subEstados, setSubEstados] = useState<SubEstadoOut[]>([]);
  const [destino, setDestino] = useState("");
  const [aplicando, setAplicando] = useState(false);
  const [resultado, setResultado] = useState<CambioMasivoResult | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api.get<EjecutivoOut[]>("/catalogos/ejecutivos").then((r) => setEjecutivos(r.data)).catch(() => setEjecutivos([]));
    api.get<SubEstadoOut[]>("/catalogos/sub_estados").then((r) => setSubEstados(r.data)).catch(() => setSubEstados([]));
  }, []);

  useEffect(() => { setDestino(""); setResultado(null); }, [accion]);

  const aplicar = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file) {
      toast.error("Elegí un archivo CSV.");
      return;
    }
    if (!destino) {
      toast.error("Elegí el destino.");
      return;
    }
    setAplicando(true);
    setResultado(null);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const url = accion === "reasignacion" ? "/cambios-masivos/reasignacion" : "/cambios-masivos/sub-estado";
      fd.append(accion === "reasignacion" ? "ejecutivo" : "id_sub_est", destino);
      const { data } = await api.post<CambioMasivoResult>(url, fd);
      setResultado(data);
      toast.success(`${data.afectadas} cuenta(s) actualizadas${data.no_encontradas.length ? `, ${data.no_encontradas.length} no encontradas` : ""}.`);
      if (fileRef.current) fileRef.current.value = "";
    } catch {
      toast.error("No se pudo aplicar el cambio.");
    } finally {
      setAplicando(false);
    }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-[var(--color-ink-soft)]">
        Subí un CSV con una columna <code>matricula</code> y elegí el destino a aplicar.
      </p>
      <div>
        <label className="form-label">Acción</label>
        <select className="form-input" value={accion} onChange={(e) => setAccion(e.target.value as Accion)}>
          <option value="reasignacion">Reasignación de cuentas</option>
          <option value="sub-estado">Cambio de sub-estado</option>
        </select>
      </div>
      <div>
        <label className="form-label">{accion === "reasignacion" ? "Ejecutivo destino" : "Sub-estado destino"}</label>
        <select className="form-input" value={destino} onChange={(e) => setDestino(e.target.value)}>
          <option value="">Elegí...</option>
          {accion === "reasignacion"
            ? ejecutivos.map((e) => <option key={e.id_usuario} value={e.id_usuario}>{e.nombre}</option>)
            : subEstados.map((s) => <option key={s.id_sub_est} value={s.id_sub_est}>{s.desc_sub_est}</option>)}
        </select>
      </div>
      <div>
        <label className="form-label">Archivo CSV (columna matricula)</label>
        <input ref={fileRef} type="file" accept=".csv" className="form-input" />
      </div>
      <button type="button" className="btn btn-warning" onClick={aplicar} disabled={aplicando}>
        {aplicando ? <><i className="fas fa-circle-notch fa-spin" /> Aplicando...</> : <><i className="fas fa-check" /> Aplicar</>}
      </button>
      {resultado && (
        <div className="border border-[var(--color-line)] rounded-lg p-3 text-sm">
          <p><strong>{resultado.afectadas}</strong> cuenta(s) actualizadas.</p>
          {resultado.no_encontradas.length > 0 && (
            <p className="text-[var(--color-danger)] mt-1 text-xs">No encontradas: {resultado.no_encontradas.join(", ")}</p>
          )}
        </div>
      )}
    </div>
  );
}
