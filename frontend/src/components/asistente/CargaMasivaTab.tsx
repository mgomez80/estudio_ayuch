import { useRef, useState } from "react";
import { api } from "../../api/client";
import { toast } from "../../store/toastStore";
import type { CargaMasivaResult } from "../../types/domain";

const ENTIDADES: { value: string; label: string; columnas: string[] }[] = [
  { value: "cuentas", label: "Cuentas", columnas: ["matricula", "nombre", "contacto", "monto_deuda", "fecha_deuda", "fecha_asignacion", "empleador", "cuenta_cliente", "id_sub_cliente", "observacion", "mora"] },
  { value: "telefonos", label: "Teléfonos", columnas: ["matricula", "tipo", "codigo_area", "numero_tel", "observaciones"] },
  { value: "direcciones", label: "Direcciones", columnas: ["matricula", "calle_dir", "nro_dir", "piso_dir", "dpto_dir", "casa_dir", "manzana_dir", "barrio_dir", "CP_dir", "localidad_dir", "departamento_dir", "provincia_dir", "seccional_dir", "tipo_dir", "observacion_dir"] },
  { value: "mails", label: "Mails", columnas: ["matricula", "mail"] },
  { value: "contactos", label: "Contactos", columnas: ["matricula", "accion", "resultado", "fecha_contacto", "hora_contacto", "nota"] },
];

interface ProcesarResult {
  promovidas: number;
  errores: { fila: number; motivo: string }[];
  vaciado: boolean;
}

const PROMOCION_SOPORTADA = new Set(["cuentas", "telefonos", "direcciones", "mails"]);

export default function CargaMasivaTab() {
  const [entidad, setEntidad] = useState("cuentas");
  const [subiendo, setSubiendo] = useState(false);
  const [procesando, setProcesando] = useState(false);
  const [resultado, setResultado] = useState<CargaMasivaResult | null>(null);
  const [resultadoProc, setResultadoProc] = useState<ProcesarResult | null>(null);
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
    try {
      const fd = new FormData();
      fd.append("file", file);
      const { data } = await api.post<CargaMasivaResult>(`/carga-masiva/${entidad}`, fd);
      setResultado(data);
      setResultadoProc(null);
      toast.success(`${data.insertadas} fila(s) cargadas${data.errores.length ? `, ${data.errores.length} con error` : ""}.`);
      if (fileRef.current) fileRef.current.value = "";
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo procesar el CSV.");
    } finally {
      setSubiendo(false);
    }
  };

  const procesar = async () => {
    setProcesando(true);
    try {
      const { data } = await api.post<ProcesarResult>(`/carga-masiva/${entidad}/procesar`);
      setResultadoProc(data);
      if (data.vaciado) {
        setResultado(null);
        toast.success(`${data.promovidas} registro(s) cargados a las tablas reales. Staging vaciado.`);
      } else {
        toast.error(`${data.errores.length} error(es). No se vació el staging; corregí y reintentá.`);
      }
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo procesar.");
    } finally {
      setProcesando(false);
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
            {resultadoProc.vaciado
              ? <span className="text-[var(--color-success)]">Staging vaciado.</span>
              : <span className="text-[var(--color-danger)]">Staging conservado (hubo errores).</span>}
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
