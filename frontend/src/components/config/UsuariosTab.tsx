import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { toast } from "../../store/toastStore";
import { ConfirmDialog } from "../ui/ConfirmDialog";
import { Modal } from "../ui/Modal";
import { TableSkeleton } from "../ui/Skeleton";
import { EmptyState } from "../ui/EmptyState";

interface UsuarioOut {
  id_usuario: number;
  loguin_usuario: string;
  nombre_completo: string | null;
  rol: string;
  activo: boolean;
  perfiles_id_perfil: number | null;
}

interface PerfilOpt {
  id_perfil: number;
  nombre: string;
}

const FORM_VACIO = { loguin_usuario: "", password: "", nombre_completo: "", rol: "gestor", perfiles_id_perfil: 0 };

export default function UsuariosTab() {
  const [usuarios, setUsuarios] = useState<UsuarioOut[]>([]);
  const [perfiles, setPerfiles] = useState<PerfilOpt[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState<UsuarioOut | null>(null);
  const [form, setForm] = useState(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);
  const [aDarBaja, setADarBaja] = useState<UsuarioOut | null>(null);

  const cargar = () => {
    setLoading(true);
    Promise.all([api.get<UsuarioOut[]>("/config/usuarios"), api.get<PerfilOpt[]>("/config/perfiles")])
      .then(([u, p]) => {
        setUsuarios(u.data);
        setPerfiles(p.data);
      })
      .catch(() => {
        setUsuarios([]);
        setPerfiles([]);
      })
      .finally(() => setLoading(false));
  };

  useEffect(cargar, []);

  const mapPerfiles = new Map(perfiles.map((p) => [p.id_perfil, p.nombre]));

  const abrirAlta = () => {
    setEditando(null);
    setForm(FORM_VACIO);
    setModalOpen(true);
  };

  const abrirEdicion = (u: UsuarioOut) => {
    setEditando(u);
    setForm({
      loguin_usuario: u.loguin_usuario,
      password: "",
      nombre_completo: u.nombre_completo ?? "",
      rol: u.rol,
      perfiles_id_perfil: u.perfiles_id_perfil ?? 0,
    });
    setModalOpen(true);
  };

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    setGuardando(true);
    try {
      if (editando == null) {
        await api.post("/config/usuarios", {
          loguin_usuario: form.loguin_usuario,
          password: form.password,
          nombre_completo: form.nombre_completo,
          rol: form.rol,
          perfiles_id_perfil: form.perfiles_id_perfil || null,
        });
        toast.success("Usuario creado.");
      } else {
        const payload: Record<string, unknown> = {
          nombre_completo: form.nombre_completo,
          rol: form.rol,
          perfiles_id_perfil: form.perfiles_id_perfil || null,
        };
        if (form.password) payload.password = form.password;
        await api.patch(`/config/usuarios/${editando.id_usuario}`, payload);
        toast.success("Usuario actualizado.");
      }
      setModalOpen(false);
      cargar();
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo guardar el usuario.");
    } finally {
      setGuardando(false);
    }
  };

  const confirmarBaja = async () => {
    if (!aDarBaja) return;
    try {
      await api.delete(`/config/usuarios/${aDarBaja.id_usuario}`);
      toast.success("Usuario dado de baja.");
      cargar();
    } catch {
      toast.error("No se pudo dar de baja el usuario.");
    } finally {
      setADarBaja(null);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between gap-2 flex-wrap mb-3">
        <h3 className="section-title text-sm">
          <i className="fas fa-user-gear" /> Usuarios
        </h3>
        <button type="button" className="btn btn-secondary btn-sm" onClick={abrirAlta}>
          <i className="fas fa-plus" /> Nuevo
        </button>
      </div>

      {loading ? (
        <TableSkeleton rows={4} cols={5} />
      ) : usuarios.length === 0 ? (
        <EmptyState icon="fa-user-gear" title="Sin usuarios" hint="Todavía no hay usuarios cargados." />
      ) : (
        <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
          <table className="data-table">
            <thead>
              <tr>
                <th>Usuario</th>
                <th>Nombre</th>
                <th>Rol</th>
                <th>Perfil</th>
                <th>Estado</th>
                <th className="text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr key={u.id_usuario}>
                  <td className="font-data">{u.loguin_usuario}</td>
                  <td>{u.nombre_completo ?? "—"}</td>
                  <td>{u.rol}</td>
                  <td>{u.perfiles_id_perfil ? mapPerfiles.get(u.perfiles_id_perfil) ?? u.perfiles_id_perfil : "—"}</td>
                  <td>{u.activo ? "Activo" : "De baja"}</td>
                  <td className="text-right whitespace-nowrap">
                    <button type="button" className="btn btn-ghost btn-sm" onClick={() => abrirEdicion(u)}>
                      <i className="fas fa-pen" /> Editar
                    </button>
                    {u.activo && (
                      <button type="button" className="btn btn-ghost-danger btn-sm" onClick={() => setADarBaja(u)}>
                        <i className="fas fa-ban" /> Baja
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editando == null ? "Nuevo usuario" : "Editar usuario"}
        icon="fa-user-gear"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancelar
            </button>
            <button type="submit" form="form-usuario" className="btn btn-success" disabled={guardando}>
              {guardando ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-usuario" onSubmit={guardar} className="space-y-3">
                <div>
                  <label className="form-label">Usuario (login)</label>
                  <input
                    type="text"
                    value={form.loguin_usuario}
                    onChange={(e) => setForm({ ...form, loguin_usuario: e.target.value })}
                    className="form-input"
                    required
                    disabled={editando != null}
                    autoFocus
                  />
                </div>
                <div>
                  <label className="form-label">{editando == null ? "Password" : "Nueva password (opcional)"}</label>
                  <input
                    type="password"
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    className="form-input"
                    required={editando == null}
                    minLength={6}
                  />
                </div>
                <div>
                  <label className="form-label">Nombre completo</label>
                  <input
                    type="text"
                    value={form.nombre_completo}
                    onChange={(e) => setForm({ ...form, nombre_completo: e.target.value })}
                    className="form-input"
                    required
                  />
                </div>
                <div>
                  <label className="form-label">Rol</label>
                  <select
                    value={form.rol}
                    onChange={(e) => setForm({ ...form, rol: e.target.value })}
                    className="form-input"
                    required
                  >
                    <option value="admin">admin</option>
                    <option value="gestor">gestor</option>
                  </select>
                </div>
                <div>
                  <label className="form-label">Perfil (permisos)</label>
                  <select
                    value={form.perfiles_id_perfil}
                    onChange={(e) => setForm({ ...form, perfiles_id_perfil: Number(e.target.value) })}
                    className="form-input"
                  >
                    <option value={0}>Sin perfil asignado</option>
                    {perfiles.map((p) => (
                      <option key={p.id_perfil} value={p.id_perfil}>
                        {p.nombre}
                      </option>
                    ))}
                  </select>
                </div>
        </form>
      </Modal>

      <ConfirmDialog
        open={aDarBaja != null}
        title="Dar de baja"
        message="¿Dar de baja este usuario?"
        confirmLabel="Dar de baja"
        onConfirm={confirmarBaja}
        onCancel={() => setADarBaja(null)}
      />
    </div>
  );
}
