import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { NAV_EXTRAJUDICIAL } from "../routes/navConfig";
import BuscadorCuentas from "../components/BuscadorCuentas";
import CuentaHeader from "../components/CuentaHeader";
import Sidebar from "./Sidebar";
import { useAuthStore } from "../store/authStore";
import { useThemeStore } from "../store/themeStore";
import { useEffect, useState } from "react";
import AsistenteIAModal from "../components/AsistenteIAModal";
import { Modal } from "../components/ui/Modal";
import CargaMasivaTab from "../components/asistente/CargaMasivaTab";
import CargaSimpleModal from "../components/CargaSimpleModal";
import CambiosMasivosTab from "../components/asistente/CambiosMasivosTab";
import ConfiguracionModal from "../components/config/ConfiguracionModal";
import { ToastHost } from "../components/ui/ToastHost";

// Acento judicial propio: NAV_JUDICIAL no define accent (usa el naranja de la sección)
const ACCENT_POR_SECCION: Record<string, string> = Object.fromEntries([
  ...NAV_EXTRAJUDICIAL.map((i) => [i.seccion, i.accent ?? "--color-brand"]),
]);

export default function AppLayout() {
  const usuario = useAuthStore((s) => s.usuario);
  const logout = useAuthStore((s) => s.logout);
  const theme = useThemeStore((s) => s.theme);
  const toggleTheme = useThemeStore((s) => s.toggle);
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const seccionActual = pathname.split("/").filter(Boolean).pop() ?? "";
  const accent = ACCENT_POR_SECCION[seccionActual] ?? "--color-brand";

  // Var a nivel documento: los modales (portal a body) también heredan el acento de la sección
  useEffect(() => {
    document.documentElement.style.setProperty("--st-accent", `var(${accent})`);
  }, [accent]);
  const [asistenteAbierto, setAsistenteAbierto] = useState(false);
  const [cargaAbierta, setCargaAbierta] = useState(false);
  const [cargaSimpleAbierta, setCargaSimpleAbierta] = useState(false);
  const [cambiosAbiertos, setCambiosAbiertos] = useState(false);
  const [configAbierta, setConfigAbierta] = useState(false);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const inicial = usuario?.loguin_usuario?.[0]?.toUpperCase() ?? "?";

  return (
    <div className="min-h-dvh">
      <header className="sticky top-0 z-30 border-b border-[var(--color-line)] bg-[var(--color-surface)]/85 backdrop-blur-md shadow-[var(--shadow-card)]">
        <div className="max-w-[1400px] mx-auto px-4 py-3 flex items-center justify-between gap-3">
          <h1 className="text-base font-bold flex items-center gap-2.5">
            <span className="grid place-items-center w-8 h-8 rounded-lg text-white bg-gradient-to-br from-[var(--color-brand)] to-[var(--color-brand-accent)] shadow-[0_4px_12px_-2px_var(--color-brand-accent)]">
              <i className="fas fa-hand-holding-dollar text-sm" />
            </span>
            Seguimiento de Deudores
          </h1>
          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setAsistenteAbierto(true)}
              className="btn btn-primary btn-sm focus-visible:ring-[var(--color-brand-accent)]"
            >
              <i className="fas fa-chart-line" /> Smart Dash
            </button>
            <button
              onClick={() => setCargaSimpleAbierta(true)}
              className="btn btn-info btn-sm focus-visible:ring-[var(--color-info)]"
            >
              <i className="fas fa-user-plus" /> Carga simple
            </button>
            <button
              onClick={() => setCargaAbierta(true)}
              className="btn btn-info btn-sm focus-visible:ring-[var(--color-info)]"
            >
              <i className="fas fa-upload" /> Carga masiva
            </button>
            <button
              onClick={() => setCambiosAbiertos(true)}
              className="btn btn-warning btn-sm focus-visible:ring-[var(--color-warning)]"
            >
              <i className="fas fa-pen-to-square" /> Cambios masivos
            </button>
            {usuario?.rol === "admin" && (
              <button
                onClick={() => setConfigAbierta(true)}
                className="btn btn-secondary btn-sm focus-visible:ring-[var(--color-brand-accent)]"
              >
                <i className="fas fa-gear" /> Configuración
              </button>
            )}
            <button
              onClick={toggleTheme}
              aria-label={theme === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
              className="btn btn-secondary btn-sm !px-2 focus-visible:ring-[var(--color-brand-accent)]"
            >
              <i className={`fas ${theme === "dark" ? "fa-sun" : "fa-moon"}`} />
            </button>
            <div className="flex items-center gap-2 pl-1">
              <span className="grid place-items-center w-7 h-7 rounded-full text-xs font-bold text-white bg-gradient-to-br from-[var(--color-brand)] to-[var(--color-brand-accent)]">
                {inicial}
              </span>
              <span className="text-xs font-medium text-[var(--color-ink-soft)] hidden sm:block">
                {usuario?.loguin_usuario}
              </span>
            </div>
            <button onClick={handleLogout} className="btn btn-ghost-danger btn-sm focus-visible:ring-[var(--color-danger)]">
              <i className="fas fa-arrow-right-from-bracket" /> Salir
            </button>
          </div>
        </div>
        <div className="max-w-[1400px] mx-auto px-4 pb-3">
          <BuscadorCuentas />
        </div>
      </header>

      <main className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
        <CuentaHeader />
        <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-4 items-start">
          <Sidebar />
          <div
            className="card card-section p-5 min-h-[440px] animate-in"
            style={{ ["--st-accent" as string]: `var(${accent})` }}
          >
            <Outlet />
          </div>
        </div>
      </main>

      {asistenteAbierto && <AsistenteIAModal onClose={() => setAsistenteAbierto(false)} />}
      <CargaSimpleModal open={cargaSimpleAbierta} onClose={() => setCargaSimpleAbierta(false)} />
      <Modal open={cargaAbierta} onClose={() => setCargaAbierta(false)} title="Carga masiva" icon="fa-upload" size="lg">
        <CargaMasivaTab />
      </Modal>
      <Modal open={cambiosAbiertos} onClose={() => setCambiosAbiertos(false)} title="Cambios masivos" icon="fa-pen-to-square" size="lg">
        <CambiosMasivosTab />
      </Modal>
      {configAbierta && <ConfiguracionModal onClose={() => setConfigAbierta(false)} />}
      <ToastHost />
    </div>
  );
}
