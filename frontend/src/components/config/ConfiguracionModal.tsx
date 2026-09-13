import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { api } from "../../api/client";
import CrudGenerico from "./CrudGenerico";
import UsuariosTab from "./UsuariosTab";
import PerfilesTab from "./PerfilesTab";

type Tab =
  | "usuarios"
  | "perfiles"
  | "clientes"
  | "subclientes"
  | "estados"
  | "sub-estados"
  | "acciones"
  | "resultados"
  | "conceptos";

const TABS: [Tab, string, string][] = [
  ["usuarios", "Usuarios", "fa-user-gear"],
  ["perfiles", "Perfiles", "fa-user-shield"],
  ["clientes", "Clientes", "fa-building"],
  ["subclientes", "Subclientes", "fa-sitemap"],
  ["estados", "Estados", "fa-flag"],
  ["sub-estados", "Subestados", "fa-flag-checkered"],
  ["acciones", "Acciones", "fa-bolt"],
  ["resultados", "Resultados", "fa-clipboard-check"],
  ["conceptos", "Conceptos", "fa-tags"],
];

export default function ConfiguracionModal({ onClose }: { onClose: () => void }) {
  const [tab, setTab] = useState<Tab>("clientes");
  const [estados, setEstados] = useState<{ id_estado: number; desc_estado: string }[]>([]);
  const [clientes, setClientes] = useState<{ id_cliente: number; cuenta_cliente: number; desc_cliente: string }[]>([]);

  useEffect(() => {
    api
      .get("/catalogos/estados")
      .then((r) => setEstados(r.data))
      .catch(() => setEstados([]));
  }, []);

  useEffect(() => {
    if (tab !== "subclientes") return;
    api
      .get("/config/clientes")
      .then((r) => setClientes(r.data))
      .catch(() => setClientes([]));
  }, [tab]);

  const opcionesEstados = estados.map((e) => ({ value: e.id_estado, label: e.desc_estado }));
  // El combo codifica "id_cliente-cuenta_cliente" en un solo value porque la PK es compuesta.
  const opcionesClientes = clientes.map((c) => ({
    value: `${c.id_cliente}-${c.cuenta_cliente}`,
    label: `${c.desc_cliente} (#${c.id_cliente}/${c.cuenta_cliente})`,
  }));

  return createPortal(
    <div className="modal-overlay" onMouseDown={onClose}>
      <div className="modal-panel max-w-4xl max-h-[85vh] overflow-hidden" onMouseDown={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="section-title text-sm">
            <i className="fas fa-gear" /> Configuración
          </h3>
          <button onClick={onClose} aria-label="Cerrar" className="btn btn-ghost btn-sm !px-2">
            <i className="fas fa-times" />
          </button>
        </div>

        <div className="flex border-b border-[var(--color-line)] text-sm overflow-x-auto">
          {TABS.map(([key, label, icon]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`px-4 py-2 border-b-2 whitespace-nowrap ${
                tab === key
                  ? "border-[var(--color-brand)] text-[var(--color-brand)] font-medium"
                  : "border-transparent text-[var(--color-ink-soft)]"
              }`}
            >
              <i className={`fas ${icon}`} /> {label}
            </button>
          ))}
        </div>

        <div className="flex-1 min-h-0 overflow-y-auto p-4">
          {tab === "usuarios" && <UsuariosTab />}
          {tab === "perfiles" && <PerfilesTab />}
          {tab === "clientes" && (
            <CrudGenerico
              titulo="Clientes"
              icono="fa-building"
              endpoint="/config/clientes"
              idFields={["id_cliente", "cuenta_cliente"]}
              campoActivo="activo"
              columnas={[
                { key: "id_cliente", label: "ID CLIENTE", tipo: "number", soloTabla: true },
                { key: "desc_cliente", label: "NOMBRE", tipo: "text", requerido: true },
              ]}
            />
          )}
          {tab === "subclientes" && (
            <CrudGenerico
              titulo="Subclientes"
              icono="fa-sitemap"
              endpoint="/config/subclientes"
              idFields={["id_subcli"]}
              campoActivo="activo_subcli"
              columnas={[
                { key: "id_subcli", label: "ID Subcliente", tipo: "number", soloTabla: true },
                { key: "nombre_subcli", label: "Subcliente", tipo: "text", requerido: true },
                { key: "cliente_nombre", label: "Cliente", tipo: "text", soloTabla: true },
                { key: "cliente", label: "Cliente", tipo: "select", opciones: opcionesClientes, requerido: true, soloForm: true },
                { key: "decuento_subcli", label: "Descuento", tipo: "text", soloForm: true },
                { key: "porccomi_subcli", label: "% Comisión", tipo: "number", soloForm: true },
                { key: "porcquita_subcli", label: "% Quita", tipo: "number", soloForm: true },
                { key: "porcact_subcli", label: "% Actualización", tipo: "number", soloForm: true },
                { key: "plazogestion_subcli", label: "Plazo gestión (días)", tipo: "number", soloForm: true },
              ]}
              transformarEnvio={(form) => {
                const { cliente, ...resto } = form;
                const [id, cuenta] = String(cliente).split("-");
                return { ...resto, clientes_id_cliente: Number(id), clientes_cuenta_cliente: Number(cuenta) };
              }}
              transformarEdicion={(item) => ({
                cliente: `${item.clientes_id_cliente}-${item.clientes_cuenta_cliente}`,
              })}
            />
          )}
          {tab === "estados" && (
            <CrudGenerico
              titulo="Estados"
              icono="fa-flag"
              endpoint="/config/estados"
              idFields={["id_estado"]}
              campoActivo="activo"
              columnas={[
                { key: "desc_estado", label: "Descripción", tipo: "text", requerido: true },
                { key: "tipo_estado", label: "Tipo", tipo: "text", requerido: true },
              ]}
            />
          )}
          {tab === "sub-estados" && (
            <CrudGenerico
              titulo="Subestados"
              icono="fa-flag-checkered"
              endpoint="/config/sub-estados"
              idFields={["id_sub_est"]}
              campoActivo="activo"
              columnas={[
                { key: "desc_sub_est", label: "Descripción", tipo: "text", requerido: true },
                { key: "estados_id_estado", label: "Estado", tipo: "select", opciones: opcionesEstados, requerido: true },
              ]}
            />
          )}
          {tab === "acciones" && (
            <CrudGenerico
              titulo="Acciones"
              icono="fa-bolt"
              endpoint="/config/acciones"
              idFields={["id_accion"]}
              campoActivo="activa"
              columnas={[{ key: "desc_accion", label: "Descripción", tipo: "text", requerido: true }]}
            />
          )}
          {tab === "resultados" && (
            <CrudGenerico
              titulo="Resultados"
              icono="fa-clipboard-check"
              endpoint="/config/resultados"
              idFields={["id_resultado"]}
              campoActivo="activo"
              columnas={[
                { key: "desc_resultado", label: "Descripción", tipo: "text", requerido: true },
                {
                  key: "positivo",
                  label: "¿Positivo?",
                  tipo: "select",
                  opciones: [
                    { value: "S", label: "Sí" },
                    { value: "N", label: "No" },
                  ],
                },
              ]}
            />
          )}
          {tab === "conceptos" && (
            <CrudGenerico
              titulo="Conceptos"
              icono="fa-tags"
              endpoint="/config/conceptos"
              idFields={["id_concepto"]}
              campoActivo="activo"
              columnas={[
                { key: "desc_concepto", label: "Descripción", tipo: "text", requerido: true },
                { key: "rubros_id_rubro", label: "ID Rubro", tipo: "number", requerido: true },
              ]}
            />
          )}
        </div>
      </div>
    </div>,
    document.body
  );
}
