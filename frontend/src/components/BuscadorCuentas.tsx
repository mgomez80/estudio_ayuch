import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAccountStore } from "../store/accountStore";
import type { CuentaDetalleOut, CuentaOut } from "../types/domain";

type Modo = "cuenta" | "documento" | "nombre";

interface Resultado {
  id_cta: number;
  razon_social_ent: string | null;
  entidades_matricula_ent: string;
  deudaact_cta: string | null;
}

// Autodetección del tipo de búsqueda según lo tipeado.
function detectar(v: string): Modo {
  const t = v.trim();
  if (/^\d+$/.test(t)) return t.length >= 7 ? "documento" : "cuenta";
  return "nombre";
}

const MIN_LEN: Record<Modo, number> = { cuenta: 1, documento: 3, nombre: 2 };
const LABEL: Record<Modo, string> = { cuenta: "N° de cuenta", documento: "Documento", nombre: "Nombre / razón social" };
const ICON: Record<Modo, string> = { cuenta: "fa-hashtag", documento: "fa-id-card", nombre: "fa-user" };

function escaparRegex(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Resalta las palabras buscadas dentro del texto del resultado.
function resaltar(texto: string, q: string) {
  const palabras = q.trim().split(/\s+/).filter(Boolean);
  if (!palabras.length) return texto;
  const re = new RegExp(`(${palabras.map(escaparRegex).join("|")})`, "gi");
  const set = new Set(palabras.map((w) => w.toLowerCase()));
  return texto.split(re).map((part, i) =>
    set.has(part.toLowerCase()) ? (
      <mark key={i} className="bg-[color-mix(in_srgb,var(--st-accent,var(--color-brand))_14%,var(--color-surface-2))] text-[var(--st-accent,var(--color-brand))] rounded px-0.5">{part}</mark>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

export default function BuscadorCuentas() {
  const [q, setQ] = useState("");
  const [resultados, setResultados] = useState<Resultado[]>([]);
  const [abierto, setAbierto] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activo, setActivo] = useState(0);
  const [abriendo, setAbriendo] = useState(false);

  const setCuenta = useAccountStore((s) => s.setCuenta);
  const setOtrasCuentas = useAccountStore((s) => s.setOtrasCuentas);
  const navigate = useNavigate();

  const boxRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const modo = detectar(q);
  const term = q.trim();
  const suficiente = term.length >= MIN_LEN[modo];

  // Búsqueda live con debounce.
  useEffect(() => {
    if (!suficiente) {
      setResultados([]);
      setLoading(false);
      return;
    }
    setLoading(true);
    const t = setTimeout(async () => {
      try {
        let filas: Resultado[] = [];
        if (modo === "cuenta") {
          const { data } = await api.get<Resultado>(`/cuentas/${term}`);
          filas = data ? [data] : [];
        } else if (modo === "documento") {
          const { data } = await api.get<Resultado[]>("/cuentas/buscar", { params: { matricula: term } });
          filas = data;
        } else {
          const { data } = await api.get<Resultado[]>("/cuentas/buscar", { params: { nombre: term } });
          filas = data;
        }
        setResultados(filas);
        setActivo(0);
      } catch {
        setResultados([]);
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [term, modo, suficiente]);

  // Cierre al hacer click afuera.
  useEffect(() => {
    const onDown = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setAbierto(false);
    };
    document.addEventListener("mousedown", onDown);
    return () => document.removeEventListener("mousedown", onDown);
  }, []);

  const abrir = async (item: Resultado) => {
    setAbriendo(true);
    try {
      const { data } = await api.get<CuentaDetalleOut>(`/cuentas/${item.id_cta}`);
      setCuenta(data);
      setOtrasCuentas(resultados as unknown as CuentaOut[]);
      setAbierto(false);
      setQ("");
      navigate(`/cuenta/${item.id_cta}/datos`);
    } catch {
      /* si falla el detalle, dejamos el dropdown abierto */
    } finally {
      setAbriendo(false);
    }
  };

  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setAbierto(true);
      setActivo((i) => Math.min(i + 1, resultados.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActivo((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (resultados[activo]) abrir(resultados[activo]);
    } else if (e.key === "Escape") {
      setAbierto(false);
    }
  };

  const mostrarPanel = abierto && suficiente;

  return (
    <div className="card p-4">
      <div ref={boxRef} className="relative">
        <div className="relative">
          <i className={`fas ${loading || abriendo ? "fa-circle-notch fa-spin" : "fa-magnifying-glass"} absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-ink-soft)]`} />
          <input
            ref={inputRef}
            className="form-input !pl-9 !pr-28"
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setAbierto(true);
            }}
            onFocus={() => setAbierto(true)}
            onKeyDown={onKey}
            placeholder="Buscar por N° de cuenta, documento o nombre..."
            role="combobox"
            aria-expanded={mostrarPanel}
            aria-controls="buscador-listbox"
            autoComplete="off"
          />
          {term.length > 0 && (
            <span className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1.5 text-[10px] uppercase tracking-wide font-bold text-[var(--st-accent,var(--color-brand))] bg-[color-mix(in_srgb,var(--st-accent,var(--color-brand))_14%,var(--color-surface-2))] rounded px-1.5 py-0.5 pointer-events-none">
              <i className={`fas ${ICON[modo]}`} /> {LABEL[modo]}
            </span>
          )}
        </div>

        {mostrarPanel && (
          <div className="absolute z-40 mt-1.5 w-full rounded-xl border border-[var(--color-line)] bg-[var(--color-surface)] shadow-[var(--shadow-pop)] overflow-hidden animate-in">
            {loading ? (
              <div className="px-4 py-5 space-y-2.5">
                <div className="skeleton h-4 w-2/3" />
                <div className="skeleton h-4 w-1/2" />
                <div className="skeleton h-4 w-3/5" />
              </div>
            ) : resultados.length === 0 ? (
              <div className="px-4 py-6 text-center">
                <i className="fas fa-magnifying-glass-minus text-lg text-[var(--color-ink-soft)] opacity-60" />
                <p className="text-sm text-[var(--color-ink-soft)] mt-1.5">Sin coincidencias para “{term}”.</p>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between px-4 py-2 border-b border-[var(--color-line)] bg-[var(--color-surface-2)]">
                  <span className="text-[10px] uppercase tracking-wider font-bold text-[var(--color-ink-soft)]">
                    {resultados.length} resultado{resultados.length !== 1 ? "s" : ""}
                  </span>
                  <span className="text-[10px] text-[var(--color-ink-soft)] hidden sm:block">
                    ↑↓ navegar · Enter abrir · Esc cerrar
                  </span>
                </div>
                <ul id="buscador-listbox" role="listbox" className="max-h-[55vh] overflow-y-auto divide-y divide-[var(--color-line)]">
                  {resultados.map((f, i) => (
                    <li key={f.id_cta} role="option" aria-selected={i === activo}>
                      <button
                        type="button"
                        onMouseDown={(e) => e.preventDefault()}
                        onMouseEnter={() => setActivo(i)}
                        onClick={() => abrir(f)}
                        className={`w-full text-left px-3.5 py-2.5 flex items-center gap-3 transition-colors ${
                          i === activo ? "bg-[color-mix(in_srgb,var(--st-accent,var(--color-brand))_10%,var(--color-surface))]" : ""
                        }`}
                      >
                        <span
                          className="grid place-items-center w-9 h-9 rounded-full text-xs font-bold text-white shrink-0"
                          style={{
                            backgroundImage:
                              "linear-gradient(135deg, var(--st-accent, var(--color-brand)), color-mix(in srgb, var(--st-accent, var(--color-brand)) 65%, white))",
                          }}
                        >
                          {(f.razon_social_ent ?? "?").trim().charAt(0).toUpperCase()}
                        </span>
                        <span className="flex-1 min-w-0">
                          <span className="block text-sm font-semibold truncate">
                            {modo === "nombre" && f.razon_social_ent ? resaltar(f.razon_social_ent, term) : f.razon_social_ent ?? "—"}
                          </span>
                          <span className="flex items-center gap-2 mt-0.5 text-xs text-[var(--color-ink-soft)]">
                            <span className="font-data inline-flex items-center gap-1">
                              <i className="fas fa-hashtag text-[9px] opacity-60" />
                              {modo === "cuenta" ? resaltar(String(f.id_cta), term) : f.id_cta}
                            </span>
                            <span className="opacity-40">·</span>
                            <span className="font-data inline-flex items-center gap-1">
                              <i className="fas fa-id-card text-[9px] opacity-60" />
                              {modo === "documento" ? resaltar(f.entidades_matricula_ent, term) : f.entidades_matricula_ent}
                            </span>
                          </span>
                        </span>
                        {f.deudaact_cta != null && (
                          <span className="text-right shrink-0">
                            <span className="block text-[9px] uppercase tracking-wide font-bold text-[var(--color-ink-soft)]">Deuda</span>
                            <span className="block text-sm font-data font-semibold text-[var(--color-danger)]">
                              $ {Number(f.deudaact_cta).toLocaleString("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                            </span>
                          </span>
                        )}
                        <i className={`fas fa-chevron-right text-xs text-[var(--st-accent,var(--color-brand))] transition-opacity ${i === activo ? "opacity-100" : "opacity-0"}`} />
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </div>

      {term.length > 0 && !suficiente && (
        <p className="text-xs text-[var(--color-ink-soft)] mt-1.5">
          Escribí al menos {MIN_LEN[modo]} caracter(es) para buscar por {LABEL[modo].toLowerCase()}.
        </p>
      )}
    </div>
  );
}
