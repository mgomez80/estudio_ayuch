import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AppLayout from "./layout/AppLayout";
import Login from "./pages/Login";
import ProtectedRoute from "./routes/ProtectedRoute";
import BuscadorInicial from "./pages/BuscadorInicial";
import SectionPlaceholder from "./pages/sections/SectionPlaceholder";
import { ErrorBoundary } from "./components/ui/ErrorBoundary";
import { TableSkeleton } from "./components/ui/Skeleton";
import { NAV_EXTRAJUDICIAL } from "./routes/navConfig";

// Code-splitting por sección
const DatosCuenta = lazy(() => import("./pages/sections/DatosCuenta"));
const TelefonosDomicilios = lazy(() => import("./pages/sections/TelefonosDomicilios"));
const Contactos = lazy(() => import("./pages/sections/Contactos"));
const InformeTelefonos = lazy(() => import("./pages/sections/InformeTelefonos"));
const InformeContactos = lazy(() => import("./pages/sections/InformeContactos"));

const TODAS_LAS_SECCIONES = [...NAV_EXTRAJUDICIAL];

const COMPONENTES: Record<string, React.ComponentType> = {
  datos: DatosCuenta,
  teldom: TelefonosDomicilios,
  contactos: Contactos,
  informe_de_telefonos: InformeTelefonos,
  informes_contactos: InformeContactos,
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<BuscadorInicial />} />

          {TODAS_LAS_SECCIONES.map((item) => {
            const Componente = COMPONENTES[item.seccion];
            return (
              <Route
                key={item.seccion}
                path={`cuenta/:idCta/${item.seccion}`}
                element={
                  Componente ? (
                    <ErrorBoundary>
                      <Suspense fallback={<TableSkeleton rows={6} cols={4} />}>
                        <Componente />
                      </Suspense>
                    </ErrorBoundary>
                  ) : (
                    <SectionPlaceholder titulo={item.label} icon={item.icon} />
                  )
                }
              />
            );
          })}

          {TODAS_LAS_SECCIONES.map((item) => {
            return (
              <Route
                key={`sin-cuenta-${item.seccion}`}
                path={item.seccion}
                element={
                  <SectionPlaceholder
                    titulo={item.label}
                    icon={item.icon}
                    hint="Seleccioná una cuenta en el buscador para ver esta sección."
                  />
                }
              />
            );
          })}
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
