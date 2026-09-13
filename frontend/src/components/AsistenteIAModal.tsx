import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { api } from "../api/client";
import type { PrioridadCuenta, EstrategiaCuenta, GenerarMensajeResult } from "../types/domain";

type Tab = "reporte" | "prioridades" | "recomendaciones" | "mensajes";

// Equivalente al modal #asistenteModal del PHP original.
// Endpoints servidos por src/routers/asistente.py (análisis heurístico de cartera).
export default function AsistenteIAModal({ onClose }: { onClose: () => void }) {
  const [tab, setTab] = useState<Tab>("reporte");
  const [prioridades, setPrioridades] = useState<PrioridadCuenta[]>([]);

  useEffect(() => {
    api
      .get("/asistente/priorizar_contactos", { params: { limite: 20 } })
      .then((r) => setPrioridades(r.data.data ?? []))
      .catch(() => setPrioridades([]));
  }, []);

  return createPortal(
    <div className="modal-overlay" onMouseDown={onClose}>
      <div
        className="modal-panel max-w-3xl max-h-[85vh] overflow-hidden"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h3 className="section-title text-sm">
            <i className="fas fa-chart-line" /> Smart Dash
          </h3>
          <button onClick={onClose} aria-label="Cerrar" className="btn btn-ghost btn-sm !px-2">
            <i className="fas fa-times" />
          </button>
        </div>

        <div className="flex border-b border-[var(--color-line)] text-sm">
          {(
            [
              ["reporte", "Reporte"],
              ["prioridades", "Prioridades"],
              ["recomendaciones", "Recomendaciones"],
              ["mensajes", "Mensajes IA"],
            ] as [Tab, string][]
          ).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`px-4 py-2 border-b-2 ${
                tab === key
                  ? "border-[var(--color-brand)] text-[var(--color-brand)] font-medium"
                  : "border-transparent text-[var(--color-ink-soft)]"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {tab === "reporte" && <ReporteTab />}
          {tab === "prioridades" && <PrioridadesTab data={prioridades} />}
          {tab === "recomendaciones" && <RecomendacionesTab />}
          {tab === "mensajes" && <MensajesTab />}
        </div>
      </div>
    </div>,
    document.body
  );
}

interface SmartDashData {
  resumen: { total: number; deuda_total: number; deuda_promedio: number; deuda_max: number };
  aging: { bucket: string; cuentas: number; deuda: number }[];
  concentracion: { top_cuentas: number; deuda_top: number; porcentaje: number };
  gestion: {
    contactos: number; por_accion: { desc: string; cant: number }[];
    por_resultado: { desc: string; cant: number }[];
    tasa_compromiso: number; sin_gestion_30d: number;
    top_gestores: { nombre: string; cant: number }[];
  };
  cobros: { por_mes: { mes: string; importe: number }[]; tendencia_pct: number | null; recuperado: number; pct_recuperado: number };
  hallazgos: { nivel: "critico" | "atencion" | "info" | "positivo"; titulo: string; detalle: string }[];
  narrativa: string;
}

const NIVEL_UI: Record<string, { clase: string; icono: string }> = {
  critico: { clase: "bg-red-100 text-red-800 border-red-300", icono: "fa-triangle-exclamation" },
  atencion: { clase: "bg-amber-100 text-amber-800 border-amber-300", icono: "fa-circle-exclamation" },
  info: { clase: "bg-slate-100 text-slate-700 border-slate-300", icono: "fa-circle-info" },
  positivo: { clase: "bg-emerald-100 text-emerald-800 border-emerald-300", icono: "fa-circle-check" },
};

const money = (v: number) => `$ ${Number(v ?? 0).toLocaleString("es-AR", { maximumFractionDigits: 0 })}`;

function ReporteTab() {
  const [dias, setDias] = useState(90);
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [subclienteId, setSubclienteId] = useState("");
  const [estadoId, setEstadoId] = useState("");
  const [usuarioId, setUsuarioId] = useState("");
  const [subclientes, setSubclientes] = useState<{ id_subcli: number; nombre_subcli: string }[]>([]);
  const [estados, setEstados] = useState<{ id_estado: number; desc_estado: string }[]>([]);
  const [usuarios, setUsuarios] = useState<{ id_usuario: number; nombre: string }[]>([]);
  const [data, setData] = useState<SmartDashData | null>(null);
  const [loading, setLoading] = useState(true);

  const cargar = (params: Record<string, string | number>) => {
    setLoading(true);
    api.get("/asistente/smart_dash", { params })
      .then((r) => setData(r.data.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    cargar({ dias: 90 });
    Promise.all([
      api.get("/catalogos/subclientes"),
      api.get("/catalogos/estados"),
      api.get("/catalogos/ejecutivos"),
    ]).then(([s, e, u]) => { setSubclientes(s.data); setEstados(e.data); setUsuarios(u.data); })
      .catch(() => undefined);
  }, []);

  const aplicar = () => {
    const p: Record<string, string | number> = {};
    if (desde && hasta) { p.desde = desde; p.hasta = hasta; } else p.dias = dias;
    if (subclienteId) p.subcliente_id = subclienteId;
    if (estadoId) p.estado_id = estadoId;
    if (usuarioId) p.usuario_id = usuarioId;
    cargar(p);
  };

  const maxMes = data ? Math.max(...data.cobros.por_mes.map((m) => m.importe), 1) : 1;
  const maxAging = data ? Math.max(...data.aging.map((b) => b.deuda), 1) : 1;

  return (
    <div className="space-y-4">
      {/* Filtros */}
      <div className="flex flex-wrap items-end gap-2 text-xs">
        <div className="flex gap-1">
          {[30, 90, 180, 365].map((d) => (
            <button key={d} type="button"
              onClick={() => { setDias(d); setDesde(""); setHasta(""); }}
              className={`px-2 py-1 rounded border ${dias === d && !desde ? "bg-[var(--color-brand)] text-white border-[var(--color-brand)]" : "border-[var(--color-line)]"}`}>
              {d}d
            </button>
          ))}
        </div>
        <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} className="form-input !py-1 !text-xs" />
        <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} className="form-input !py-1 !text-xs" />
        <select value={subclienteId} onChange={(e) => setSubclienteId(e.target.value)} className="form-input !py-1 !text-xs">
          <option value="">Subcliente: todos</option>
          {subclientes.map((s) => <option key={s.id_subcli} value={s.id_subcli}>{s.nombre_subcli}</option>)}
        </select>
        <select value={estadoId} onChange={(e) => setEstadoId(e.target.value)} className="form-input !py-1 !text-xs">
          <option value="">Estado: todos</option>
          {estados.map((s) => <option key={s.id_estado} value={s.id_estado}>{s.desc_estado}</option>)}
        </select>
        <select value={usuarioId} onChange={(e) => setUsuarioId(e.target.value)} className="form-input !py-1 !text-xs">
          <option value="">Gestor: todos</option>
          {usuarios.map((u) => <option key={u.id_usuario} value={u.id_usuario}>{u.nombre}</option>)}
        </select>
        <button type="button" onClick={aplicar} className="btn btn-info btn-sm" disabled={loading}>
          <i className="fas fa-filter" /> Aplicar
        </button>
      </div>

      {loading ? <Spinner texto="Minando patrones de la cartera..." /> : !data ? <ErrorBox /> : (
        <>
          {/* Narrativa ejecutiva */}
          <div className="border-l-4 border-[var(--color-brand)] bg-[var(--color-brand-soft)] rounded-md p-3 text-sm leading-relaxed">
            <i className="fas fa-wand-magic-sparkles mr-2 text-[var(--color-brand)]" />
            {data.narrativa}
          </div>

          {/* KPIs */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { l: "Cuentas", v: data.resumen.total },
              { l: "Deuda total", v: money(data.resumen.deuda_total) },
              { l: "Recuperado en período", v: money(data.cobros.recuperado) },
              { l: "Tasa de compromiso", v: `${data.gestion.tasa_compromiso}%` },
            ].map((k) => (
              <div key={k.l} className="border-l-4 border-[var(--color-brand)] rounded-md bg-[var(--color-brand-soft)] p-3">
                <div className="text-lg font-semibold font-data">{k.v}</div>
                <div className="text-xs text-[var(--color-ink-soft)]">{k.l}</div>
              </div>
            ))}
          </div>

          {/* Hallazgos */}
          {data.hallazgos.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-semibold">Hallazgos detectados</h4>
              {data.hallazgos.map((h, i) => {
                const ui = NIVEL_UI[h.nivel] ?? NIVEL_UI.info;
                return (
                  <div key={`${h.nivel}-${h.titulo}-${i}`} className={`border rounded-md p-2 text-xs flex gap-2 ${ui.clase}`}>
                    <i className={`fas ${ui.icono} mt-0.5`} />
                    <div><strong>{h.titulo}.</strong> {h.detalle}</div>
                  </div>
                );
              })}
            </div>
          )}

          <div className="grid md:grid-cols-2 gap-4">
            {/* Aging: barras CSS */}
            <div>
              <h4 className="text-sm font-semibold mb-2">Antigüedad de la deuda</h4>
              {data.aging.map((b) => (
                <div key={b.bucket} className="flex items-center gap-2 mb-1 text-xs">
                  <span className="w-12 text-right font-data">{b.bucket}</span>
                  <div className="flex-1 bg-[var(--color-line)] rounded h-4 overflow-hidden">
                    <div className="h-4 bg-[var(--color-brand)]" style={{ width: `${(b.deuda / maxAging) * 100}%` }} />
                  </div>
                  <span className="w-28 font-data text-right">{money(b.deuda)} ({b.cuentas})</span>
                </div>
              ))}
              <p className="text-xs text-[var(--color-ink-soft)] mt-2">
                Concentración: el top {data.concentracion.top_cuentas} cuentas acumula el{" "}
                <strong>{data.concentracion.porcentaje}%</strong> de la deuda ({money(data.concentracion.deuda_top)}).
              </p>
              <div className="w-full bg-[var(--color-line)] rounded h-2 mt-1 overflow-hidden">
                <div className="h-2 bg-amber-500" style={{ width: `${data.concentracion.porcentaje}%` }} />
              </div>
            </div>

            {/* Cobros por mes: mini bar chart SVG */}
            <div>
              <h4 className="text-sm font-semibold mb-2">
                Recaudación mensual{" "}
                {data.cobros.tendencia_pct !== null && (
                  <span className={data.cobros.tendencia_pct >= 0 ? "text-emerald-600" : "text-red-600"}>
                    <i className={`fas ${data.cobros.tendencia_pct >= 0 ? "fa-arrow-trend-up" : "fa-arrow-trend-down"}`} />{" "}
                    {data.cobros.tendencia_pct}%
                  </span>
                )}
              </h4>
              {data.cobros.por_mes.length === 0 ? (
                <p className="text-xs text-[var(--color-ink-soft)]">Sin cobros en el período.</p>
              ) : (
                <svg viewBox={`0 0 ${data.cobros.por_mes.length * 44} 90`} className="w-full h-28">
                  {data.cobros.por_mes.map((m, i) => {
                    const h = (m.importe / maxMes) * 60;
                    return (
                      <g key={m.mes}>
                        <rect x={i * 44 + 6} y={70 - h} width={30} height={h} rx={2} fill="var(--color-brand)" />
                        <text x={i * 44 + 21} y={82} textAnchor="middle" fontSize="7" fill="currentColor">{m.mes.slice(2)}</text>
                        <text x={i * 44 + 21} y={70 - h - 3} textAnchor="middle" fontSize="6" fill="currentColor">{Math.round(m.importe / 1000)}k</text>
                      </g>
                    );
                  })}
                </svg>
              )}
              {data.gestion.top_gestores.length > 0 && (
                <p className="text-xs text-[var(--color-ink-soft)] mt-2">
                  Top gestión: {data.gestion.top_gestores.map((g) => `${g.nombre} (${g.cant})`).join(" · ")}
                </p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function PrioridadesTab({ data }: { data: PrioridadCuenta[] }) {
  const [detalle, setDetalle] = useState<EstrategiaCuenta | null>(null);
  const [cargandoDetalle, setCargandoDetalle] = useState(false);

  async function verDetalle(id_cta: number) {
    setCargandoDetalle(true);
    setDetalle(null);
    try {
      const { data } = await api.get(`/asistente/estrategia/${id_cta}`);
      setDetalle(data.data ?? null);
    } finally {
      setCargandoDetalle(false);
    }
  }

  if (!data.length) return <p className="text-sm text-[var(--color-ink-soft)] text-center py-8">Sin datos.</p>;

  return (
    <div className="space-y-3">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-xs text-[var(--color-ink-soft)] border-b border-[var(--color-line)]">
            <th className="py-1.5">Prio.</th>
            <th>Nombre</th>
            <th>Deuda</th>
            <th>Score</th>
            <th>Señales</th>
          </tr>
        </thead>
        <tbody>
          {data.map((c) => (
            <tr
              key={c.id_cta}
              className="border-b border-[var(--color-line)] cursor-pointer hover:bg-[var(--color-brand-soft)]"
              onClick={() => verDetalle(c.id_cta)}
            >
              <td className="py-1.5">{c.nivel_prioridad}</td>
              <td>{c.nombre}</td>
              <td className="font-data">$ {Number(c.deuda).toLocaleString("es-AR")}</td>
              <td className="font-data">{c.score_prioridad}</td>
              <td className="space-x-1">
                {c.señales.judicial_activa && <span title="Judicial activa">🏛️</span>}
                {c.señales.convenio_caido && <span title="Convenio caído">📉</span>}
                {c.señales.promesa_incumplida && <span title="Promesa incumplida">🤞</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {cargandoDetalle && <p className="text-sm text-[var(--color-ink-soft)]">Cargando detalle...</p>}

      {detalle && (
        <div className="border border-[var(--color-line)] rounded-md p-3 space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="font-semibold">{detalle.nombre} — {detalle.nivel_prioridad} ({detalle.score_prioridad})</span>
            <button onClick={() => setDetalle(null)} className="text-[var(--color-ink-soft)] hover:text-[var(--color-ink)]">
              <i className="fas fa-times" />
            </button>
          </div>
          <p><strong>Próxima acción:</strong> {detalle.proxima_accion}</p>
          <p className="text-xs text-[var(--color-ink-soft)]">
            Antigüedad de mora: {detalle.señales.antiguedad_dias} día(s) · Gestiones previas: {detalle.señales.gestiones_previas}
            {" "}(sin resultado: {detalle.señales.gestiones_sin_resultado})
          </p>
          <p className="text-xs">
            Plan sugerido: {detalle.plan_sugerido.cant_cuotas} cuotas de $ {detalle.plan_sugerido.importe_cuota.toLocaleString("es-AR")},
            {" "}anticipo $ {detalle.plan_sugerido.anticipo_sugerido.toLocaleString("es-AR")}
          </p>
          {!detalle.compliance.horario_ok && (
            <p className="text-xs text-[var(--color-warning)]">⚠ Fuera de horario de contacto ({detalle.compliance.motivo}).</p>
          )}
          {detalle.compliance.ya_contactado_hoy && (
            <p className="text-xs text-[var(--color-warning)]">⚠ Ya se registró un contacto hoy con esta cuenta.</p>
          )}
        </div>
      )}
    </div>
  );
}

function RecomendacionesTab() {
  const [items, setItems] = useState<{ titulo: string; detalle: string }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/asistente/recomendaciones")
      .then((r) => setItems(r.data.data ?? []))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Spinner texto="Cargando recomendaciones..." />;
  if (!items.length) return <p className="text-sm text-[var(--color-ink-soft)] text-center py-8">Sin recomendaciones.</p>;

  return (
    <ul className="space-y-2">
      {items.map((it, i) => (
        <li key={i} className="border-l-4 border-[var(--color-brand)] rounded-md bg-[var(--color-brand-soft)] p-3">
          <div className="text-sm font-semibold">{it.titulo}</div>
          <div className="text-xs text-[var(--color-ink-soft)] mt-0.5">{it.detalle}</div>
        </li>
      ))}
    </ul>
  );
}

function MensajesTab() {
  const [idCta, setIdCta] = useState("");
  const [tipo, setTipo] = useState("PRIMER_CONTACTO");
  const [tono, setTono] = useState("profesional");
  const [mensaje, setMensaje] = useState("");
  const [plan, setPlan] = useState<GenerarMensajeResult["plan_sugerido"] | null>(null);
  const [advertencia, setAdvertencia] = useState<string | null>(null);
  const [generando, setGenerando] = useState(false);

  async function generar() {
    if (!idCta) return;
    setGenerando(true);
    try {
      const { data } = await api.post("/asistente/generar_mensaje", { id_cta: idCta, tipo, tono });
      const resultado: GenerarMensajeResult = data.data ?? { mensaje: "" };
      setMensaje(resultado.mensaje ?? "");
      setPlan(resultado.plan_sugerido ?? null);
      setAdvertencia(resultado.advertencia ?? null);
    } finally {
      setGenerando(false);
    }
  }

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="block text-xs font-semibold mb-1">ID Cuenta</label>
          <input
            className="w-full rounded-md border border-[var(--color-line)] px-2 py-1.5 text-sm"
            value={idCta}
            onChange={(e) => setIdCta(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-xs font-semibold mb-1">Tipo de mensaje</label>
          <select
            className="w-full rounded-md border border-[var(--color-line)] px-2 py-1.5 text-sm"
            value={tipo}
            onChange={(e) => setTipo(e.target.value)}
          >
            <option value="PRIMER_CONTACTO">Primer Contacto</option>
            <option value="RECORDATORIO">Recordatorio</option>
            <option value="NEGOCIACION">Negociación</option>
            <option value="FINAL">Último aviso</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-semibold mb-1">Tono</label>
          <select
            className="w-full rounded-md border border-[var(--color-line)] px-2 py-1.5 text-sm"
            value={tono}
            onChange={(e) => setTono(e.target.value)}
          >
            <option value="profesional">Profesional</option>
            <option value="cordial">Cordial</option>
            <option value="urgente">Urgente</option>
            <option value="empatico">Empático</option>
          </select>
        </div>
      </div>
      <button
        onClick={generar}
        disabled={generando}
        className="rounded-md bg-[var(--color-brand)] text-white text-sm px-4 py-1.5 disabled:opacity-60"
      >
        {generando ? "Generando..." : "Generar mensaje con IA"}
      </button>
      {mensaje && (
        <textarea
          readOnly
          value={mensaje}
          rows={3}
          className="w-full rounded-md border border-[var(--color-line)] px-2 py-1.5 text-sm"
        />
      )}
      {plan && (
        <p className="text-xs text-[var(--color-ink-soft)]">
          Plan sugerido: {plan.cant_cuotas} cuotas de $ {plan.importe_cuota.toLocaleString("es-AR")},
          {" "}anticipo $ {plan.anticipo_sugerido.toLocaleString("es-AR")}
        </p>
      )}
      {advertencia && (
        <p className="text-xs text-[var(--color-warning)]">⚠ {advertencia}</p>
      )}
    </div>
  );
}

function Spinner({ texto }: { texto: string }) {
  return <p className="text-sm text-[var(--color-ink-soft)] text-center py-8">{texto}</p>;
}
function ErrorBox() {
  return <p className="text-sm text-[var(--color-danger)] text-center py-8">Error al cargar.</p>;
}
