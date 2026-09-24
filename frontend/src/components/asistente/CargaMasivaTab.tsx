import { useRef, useState } from "react";
import { api } from "../../api/client";
import { toast } from "../../store/toastStore";
import type { CargaMasivaResult, ProcesarCargaResult } from "../../types/domain";

const ENTIDADES: { value: string; label: string; columnas: string[] }[] = [
  { value: "cuentas", label: "Cuentas", columnas: ["matricula", "nombre", "contacto", "monto_deuda", "fecha_deuda", "fecha_asignacion", "empleador", "cuenta_cliente", "id_sub_cliente", "observacion", "mora"] },
  { value: "telefonos", label: "Teléfonos", columnas: ["matricula", "tipo", "codigo_area", "numero_tel", "observaciones"] },
  { value: "direcciones", label: "Direcciones", columnas: ["matricula", "calle_dir", "nro_dir", "piso_dir", "dpto_dir", "casa_dir", "manzana_dir", "barrio_dir", "CP_dir", "localidad_dir", "departamento_dir", "provincia_dir", "seccional_dir", "tipo_dir", "observacion_dir"] },
  { value: "mails", label: "Mails", columnas: ["matricula", "mail"] },
  { value: "contactos", label: "Contactos", columnas: ["matricula", "accion", "resultado", "fecha_contacto", "hora_contacto", "nota"] },
];

// Tamaño de tanda para subir/procesar: evita que una carga grande agote el
// timeout del proxy (nginx/Apache) en un único request de varios cientos de filas.
const LOTE = 200;

const PROMOCION_SOPORTADA = new Set(["cuentas", "telefonos", "direcciones", "mails"]);

export default function CargaMasivaTab() {
  const [entidad, setEntidad] = useState("cuentas");
  const [subiendo, setSubiendo] = useState(false);
  const [procesando, setProcesando] = useState(false);
  const [progreso, setProgreso] = useState<{ actual: number; total: number } | null>(null);
  const [resultado, setResultado] = useState<CargaMasivaResult | null>(null);
  const [resultadoProc, setResultadoProc] = useState<ProcesarCargaResult | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const cfg = ENTIDADES.find((e) => e.value === entidad)!;

  const descargarPlantilla = () => {
    const csv = cfg.columnas.join(";") + "\n";
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `plantilla_${entidad}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const subir = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file) {
      toast.error("Elegí un archivo CSV.");
      return;
    }
    setSubiendo(true);
    setResultado(null);
    setResultadoProc(null);
    try {
      const texto = await file.text();
      const lineas = texto.split(/\r\n|\r|\n/).filter((l) => l.trim() !== "");
      if (lineas.length === 0) {
        toast.error("El CSV está vacío.");
        return;
      }

      // Se sube en tandas de LOTE líneas: un archivo de varios cientos de filas
      // en un único request puede superar el timeout del proxy.
      const tandas: string[][] = [];
      for (let i = 0; i < lineas.length; i += LOTE) tandas.push(lineas.slice(i, i + LOTE));

      let insertadas = 0;
      const errores: { fila: number; motivo: string }[] = [];
      for (let t = 0; t < tandas.length; t++) {
        setProgreso({ actual: t + 1, total: tandas.length });
        const blob = new Blob([tandas[t].join("\n")], { type: "text/csv" });
        const fd = new FormData();
        fd.append("file", blob, file.name);
        const { data } = await api.post<CargaMasivaResult>(`/carga-masiva/${entidad}`, fd);
        insertadas += data.insertadas;
        const offset = t * LOTE;
        errores.push(...data.errores.map((e) => ({ ...e, fila: e.fila + offset })));
      }

      setResultado({ insertadas, errores });
      toast.success(`${insertadas} fila(s) cargadas${errores.length ? `, ${errores.length} con error` : ""}.`);
      if (fileRef.current) fileRef.current.value = "";
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo procesar el CSV.");
    } finally {
      setSubiendo(false);
      setProgreso(null);
    }
  };

  const procesar = async () => {
    setProcesando(true);
    setResultadoProc(null);
    try {
      let promovidas = 0;
      const errores: { fila: number; motivo: string }[] = [];
      let restantes = 0;
      // Llama al endpoint repetidas veces (tandas de LOTE filas) hasta vaciar el
      // staging. Si una tanda no logra promover nada, corta para no loopear
      // infinito sobre filas que siempre van a fallar (quedan para corregir).
      while (true) {
        const { data } = await api.post<ProcesarCargaResult>(
          `/carga-masiva/${entidad}/procesar`,
          null,
          { params: { lote: LOTE } }
        );
        promovidas += data.promovidas;
        errores.push(...data.errores);
        restantes = data.restantes;
        setProgreso({ actual: promovidas + errores.length, total: promovidas + errores.length + restantes });
        if (data.promovidas === 0 || restantes === 0) break;
      }

      setResultadoProc({ promovidas, errores, restantes });
      if (restantes === 0) {
        setResultado(null);
        toast.success(`${promovidas} registro(s) cargados a las tablas reales. Staging vaciado.`);
      } else {
        toast.error(`${errores.length} error(es). Esas filas quedaron en el staging; corregí y reintentá.`);
      }
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo procesar.");
    } finally {
      setProcesando(false);
      setProgreso(null);
    }
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-[var(--color-ink-soft)]">
        Cargá un CSV (separador <code>;</code> o <code>,</code>). Importa <strong>por orden de columnas</strong>;
        el encabezado es opcional. Orden esperado:
      </p>
      <p className="text-xs font-data text-[var(--color-ink-soft)] bg-[var(--color-brand-soft)] rounded-md px-2 py-1.5">
        {cfg.columnas.map((c, i) => `${i + 1}. ${c}`).join("   ")}
      </p>
      <div>
        <label className="form-label">Entidad</label>
        <select className="form-input" value={entidad} onChange={(e) => { setEntidad(e.target.value); setResultado(null); }}>
          {ENTIDADES.map((e) => <option key={e.value} value={e.value}>{e.label}</option>)}
        </select>
      </div>
      <div>
        <label className="form-label">Archivo CSV</label>
        <input ref={fileRef} type="file" accept=".csv" className="form-input" />
      </div>
      <div className="flex items-center gap-2">
        <button type="button" className="btn btn-info" onClick={subir} disabled={subiendo}>
          {subiendo ? <><i className="fas fa-circle-notch fa-spin" /> Subiendo...</> : <><i className="fas fa-upload" /> Subir</>}
        </button>
        <button type="button" className="btn btn-secondary" onClick={descargarPlantilla}>
          <i className="fas fa-download" /> Descargar plantilla
        </button>
        {PROMOCION_SOPORTADA.has(entidad) && (
          <button type="button" className="btn btn-success" onClick={procesar} disabled={procesando} title="Promueve el staging a las tablas reales y lo vacía">
            {procesando ? <><i className="fas fa-circle-notch fa-spin" /> Procesando...</> : <><i className="fas fa-database" /> Procesar a tablas reales</>}
          </button>
        )}
      </div>
      {progreso && (subiendo || procesando) && (
        <div className="text-xs text-[var(--color-ink-soft)]">
          <div className="h-1.5 rounded-full bg-[var(--color-brand-soft)] overflow-hidden">
            <div
              className="h-full bg-[var(--color-brand)] transition-all"
              style={{ width: `${Math.min(100, Math.round((progreso.actual / progreso.total) * 100))}%` }}
            />
          </div>
          <p className="mt-1">{progreso.actual} / {progreso.total}</p>
        </div>
      )}
      {resultado && (
        <div className="border border-[var(--color-line)] rounded-lg p-3 text-sm">
          <p><strong>{resultado.insertadas}</strong> fila(s) insertadas.</p>
          {resultado.errores.length > 0 && (
            <div className="mt-2">
              <p className="text-[var(--color-danger)] font-medium">{resultado.errores.length} error(es):</p>
              <ul className="mt-1 max-h-40 overflow-y-auto text-xs">
                {resultado.errores.map((er, i) => <li key={i}>Fila {er.fila}: {er.motivo}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
      {resultadoProc && (
        <div className="border border-[var(--color-line)] rounded-lg p-3 text-sm">
          <p>
            <strong>{resultadoProc.promovidas}</strong> registro(s) promovidos a tablas reales.{" "}
            {resultadoProc.restantes === 0
              ? <span className="text-[var(--color-success)]">Staging vaciado.</span>
              : <span className="text-[var(--color-danger)]">Quedan {resultadoProc.restantes} fila(s) en el staging (con error).</span>}
          </p>
          {resultadoProc.errores.length > 0 && (
            <div className="mt-2">
              <p className="text-[var(--color-danger)] font-medium">{resultadoProc.errores.length} error(es):</p>
              <ul className="mt-1 max-h-40 overflow-y-auto text-xs">
                {resultadoProc.errores.map((er, i) => <li key={i}>Fila {er.fila}: {er.motivo}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
