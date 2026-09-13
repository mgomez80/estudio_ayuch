import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { toast } from "../../store/toastStore";
import { EmptyState } from "../ui/EmptyState";

interface PerfilOut {
  id_perfil: number;
  nombre: string;
  activo: string;
}

interface ModuloOut {
  id_modulo: number;
  clave: string;
  desc_modulo: string;
}

interface PermisoFila {
  modulos_id_modulo: number;
  ver: string;
  alta: string;
  baja: string;
  modificar: string;
}

const ACCIONES: (keyof Omit<PermisoFila, "modulos_id_modulo">)[] = ["ver", "alta", "baja", "modificar"];

export default function PerfilesTab() {
  const [perfiles, setPerfiles] = useState<PerfilOut[]>([]);
  const [modulos, setModulos] = useState<ModuloOut[]>([]);
  const [seleccionado, setSeleccionado] = useState<number | null>(null);
  const [permisos, setPermisos] = useState<PermisoFila[]>([]);
  const [nombreNuevo, setNombreNuevo] = useState("");
  const [guardando, setGuardando] = useState(false);

  const cargarListas = () => {
    Promise.all([api.get<PerfilOut[]>("/config/perfiles"), api.get<ModuloOut[]>("/config/modulos")]).then(
      ([p, m]) => {
        setPerfiles(p.data);
        setModulos(m.data);
      }
    );
  };

  useEffect(cargarListas, []);

  const seleccionar = (idPerfil: number) => {
    setSeleccionado(idPerfil);
    api.get(`/config/perfiles/${idPerfil}`).then((r) => {
      const existentes = new Map<number, PermisoFila>(
        r.data.permisos.map((p: PermisoFila) => [p.modulos_id_modulo, p])
      );
      // Completa con "N" los módulos que este perfil todavía no tiene fila (perfil nuevo).
      setPermisos(
        modulos.map(
          (m) =>
            existentes.get(m.id_modulo) ?? {
              modulos_id_modulo: m.id_modulo,
              ver: "N",
              alta: "N",
              baja: "N",
              modificar: "N",
            }
        )
      );
    });
  };

  const toggle = (idModulo: number, accion: keyof Omit<PermisoFila, "modulos_id_modulo">) => {
    setPermisos((prev) =>
      prev.map((p) => (p.modulos_id_modulo === idModulo ? { ...p, [accion]: p[accion] === "S" ? "N" : "S" } : p))
    );
  };

  const crearPerfil = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nombreNuevo.trim()) return;
    try {
      const { data } = await api.post("/config/perfiles", { nombre: nombreNuevo.trim() });
      toast.success("Perfil creado.");
      setNombreNuevo("");
      cargarListas();
      seleccionar(data.id_perfil);
    } catch {
      toast.error("No se pudo crear el perfil.");
    }
  };

  const guardarPermisos = async () => {
    if (!seleccionado) return;
    setGuardando(true);
    try {
      await api.put(`/config/perfiles/${seleccionado}/permisos`, permisos);
      toast.success("Permisos actualizados.");
    } catch {
      toast.error("No se pudieron guardar los permisos.");
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-[220px_1fr] gap-4">
      <div>
        <h3 className="section-title text-sm mb-2">
          <i className="fas fa-user-shield" /> Perfiles
        </h3>
        <ul className="space-y-1 mb-3">
          {perfiles.map((p) => (
            <li key={p.id_perfil}>
              <button
                type="button"
                onClick={() => seleccionar(p.id_perfil)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm ${
                  seleccionado === p.id_perfil
                    ? "bg-[var(--color-brand)] text-white"
                    : "hover:bg-[var(--color-surface-soft)]"
                }`}
              >
                {p.nombre} {p.activo === "N" && "(inactivo)"}
              </button>
            </li>
          ))}
        </ul>
        <form onSubmit={crearPerfil} className="flex gap-1">
          <input
            type="text"
            value={nombreNuevo}
            onChange={(e) => setNombreNuevo(e.target.value)}
            placeholder="Nuevo perfil..."
            className="form-input text-sm"
          />
          <button type="submit" className="btn btn-secondary btn-sm !px-2">
            <i className="fas fa-plus" />
          </button>
        </form>
      </div>

      <div>
        {seleccionado == null ? (
          <EmptyState icon="fa-user-shield" title="Elegí un perfil" hint="Seleccioná un perfil de la lista para ver/editar su matriz de permisos." />
        ) : (
          <>
            <div className="overflow-x-auto rounded-lg border border-[var(--color-line)] mb-3">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Módulo</th>
                    {ACCIONES.map((a) => (
                      <th key={a} className="text-center capitalize">
                        {a}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {modulos.map((m) => {
                    const fila = permisos.find((p) => p.modulos_id_modulo === m.id_modulo);
                    return (
                      <tr key={m.id_modulo}>
                        <td>{m.desc_modulo}</td>
                        {ACCIONES.map((a) => (
                          <td key={a} className="text-center">
                            <input
                              type="checkbox"
                              checked={fila?.[a] === "S"}
                              onChange={() => toggle(m.id_modulo, a)}
                            />
                          </td>
                        ))}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
            <button type="button" className="btn btn-success btn-sm" onClick={guardarPermisos} disabled={guardando}>
              {guardando ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar permisos</>}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
