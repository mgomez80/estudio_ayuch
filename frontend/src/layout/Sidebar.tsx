import { useState } from "react";
import { NavLink, useParams } from "react-router-dom";
import { NAV_EXTRAJUDICIAL } from "../routes/navConfig";

// Módulo judicial oculto a pedido; poner en true para volver a mostrarlo
const MOSTRAR_JUDICIAL = false;

// Secciones ocultas del sidebar a pedido (rutas/componentes quedan intactos, solo se saca el link)
const SECCIONES_OCULTAS = new Set(["vencimientos", "chat_cobranza", "whatsapp_panel", "manejo_whatsapp"]);

export default function Sidebar() {
  const { idCta } = useParams();
  const [judicialAbierto, setJudicialAbierto] = useState(false);

  const renderItem = (item: (typeof NAV_EXTRAJUDICIAL)[number], judicial = false) => {
    const contenido = (
      <>
        <i
          className={`fas ${item.icon} w-4 text-center nav-icon`}
          style={item.accent ? { ["--nav-accent" as string]: `var(${item.accent})` } : undefined}
        />
        <span className="flex-1">{item.label}</span>
        {!item.implementado && (
          <span className="text-[9px] uppercase tracking-wide font-bold px-1.5 py-0.5 rounded bg-[var(--color-warning-soft)] text-[var(--color-warning)]">
            pronto
          </span>
        )}
      </>
    );
    const base = `nav-pill ${judicial ? "nav-pill-judicial" : ""}`;

    if (item.externalBlank && item.href) {
      return (
        <a key={item.seccion} href={item.href} target="_blank" rel="noopener noreferrer" className={base}>
          {contenido}
        </a>
      );
    }

    const to = idCta ? `/cuenta/${idCta}/${item.seccion}` : `/${item.seccion}`;
    return (
      <NavLink
        key={item.seccion}
        to={to}
        className={({ isActive }) => `${base} ${isActive ? "active" : ""}`}
      >
        {contenido}
      </NavLink>
    );
  };

  return (
    <nav className="card p-3 flex flex-col gap-4 lg:sticky lg:top-[150px]">
      <div>
        <div className="text-[11px] font-bold text-[var(--color-ink-soft)] uppercase tracking-wider px-2 mb-2 flex items-center gap-1.5">
          <i className="fas fa-folder-open text-[var(--color-brand)]" /> Gestión
        </div>
        <div className="flex flex-col gap-0.5">
          {NAV_EXTRAJUDICIAL.filter((item) => !SECCIONES_OCULTAS.has(item.seccion)).map((item) => renderItem(item))}
        </div>
      </div>

      {MOSTRAR_JUDICIAL && (
        <div className="border-t border-[var(--color-line)] pt-3">
          <button
            type="button"
            onClick={() => setJudicialAbierto((v) => !v)}
            className="w-full flex items-center justify-between px-2 py-1.5 text-[11px] font-bold text-[var(--color-judicial)] uppercase tracking-wider rounded-lg hover:bg-[var(--color-judicial-soft)] transition-colors"
          >
            <span className="flex items-center gap-1.5">
              <i className="fas fa-gavel" /> Judicial
            </span>
            <i className={`fas fa-chevron-down text-[10px] transition-transform duration-200 ${judicialAbierto ? "rotate-180" : ""}`} />
          </button>
          {judicialAbierto && (
            <div className="flex flex-col gap-0.5 mt-1 animate-in">
              {/* El módulo judicial no está definido en navConfig de Ayuch */}
            </div>
          )}
        </div>
      )}
    </nav>
  );
}
