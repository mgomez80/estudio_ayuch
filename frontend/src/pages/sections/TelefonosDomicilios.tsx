import { useCallback, useEffect, useState } from "react";
import { api } from "../../api/client";
import { useAccountStore } from "../../store/accountStore";
import type { TelefonoOut, DireccionOut, MailAbmOut } from "../../types/domain";
import { Modal } from "../../components/ui/Modal";
import { FlagBadge } from "../../components/ui/Badge";
import { TableSkeleton } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { ConfirmDialog } from "../../components/ui/ConfirmDialog";
import { StatCard } from "../../components/ui/StatCard";
import { toast } from "../../store/toastStore";

const FORM_TEL_VACIO = { tipo_tel: "", codigo_area_tel: "", numero_tel: "", observaciones_tel: "" };
const FORM_DIR_VACIO = { calle_dir: "", nro_dir: "", piso_dir: "", dpto_dir: "", barrio_dir: "", cp_dir: "", localidad_dir: "", departamento_dir: "", provincia_dir: "", tipo_dir: "", observacion_dir: "" };
const FORM_MAIL_VACIO = { mail: "", tipo_mail: "" };

const PROVINCIAS = [
  "Buenos Aires", "CABA", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes",
  "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones",
  "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe",
  "Santiago del Estero", "Tierra del Fuego", "Tucumán",
];

export default function TelefonosDomicilios() {
  const matricula = useAccountStore((s) => s.cuenta?.entidades_matricula_ent);
  const [telefonos, setTelefonos] = useState<TelefonoOut[]>([]);
  const [direcciones, setDirecciones] = useState<DireccionOut[]>([]);
  const [mails, setMails] = useState<MailAbmOut[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal ABM Teléfono
  const [modalTelOpen, setModalTelOpen] = useState(false);
  const [editTelId, setEditTelId] = useState<number | null>(null);
  const [formTel, setFormTel] = useState(FORM_TEL_VACIO);
  const [guardandoTel, setGuardandoTel] = useState(false);

  // Modal ABM Domicilio
  const [modalDirOpen, setModalDirOpen] = useState(false);
  const [editDirId, setEditDirId] = useState<number | null>(null);
  const [formDir, setFormDir] = useState(FORM_DIR_VACIO);
  const [guardandoDir, setGuardandoDir] = useState(false);

  // Modal ABM Mail
  const [modalMailOpen, setModalMailOpen] = useState(false);
  const [editMailId, setEditMailId] = useState<number | null>(null);
  const [formMail, setFormMail] = useState(FORM_MAIL_VACIO);
  const [guardandoMail, setGuardandoMail] = useState(false);

  // Confirmación de baja
  const [aDarBajaTel, setABajaTel] = useState<TelefonoOut | null>(null);
  const [aDarBajaDir, setABajaDir] = useState<DireccionOut | null>(null);
  const [aDarBajaMail, setABajaMail] = useState<MailAbmOut | null>(null);

  const cargar = useCallback(() => {
    if (!matricula) return;
    setLoading(true);
    Promise.all([
      api.get<TelefonoOut[]>(`/entidades/${matricula}/telefonos`),
      api.get<DireccionOut[]>(`/entidades/${matricula}/direcciones`),
      api.get<MailAbmOut[]>(`/entidades/${matricula}/mails`),
    ])
      .then(([tel, dir, mail]) => {
        setTelefonos(tel.data);
        setDirecciones(dir.data);
        setMails(mail.data);
      })
      .finally(() => setLoading(false));
  }, [matricula]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const abrirAltaTel = () => {
    setEditTelId(null);
    setFormTel(FORM_TEL_VACIO);
    setModalTelOpen(true);
  };

  const abrirEdicionTel = (tel: TelefonoOut) => {
    setEditTelId(tel.id_tel);
    setFormTel({
      tipo_tel: tel.tipo_tel ?? "",
      codigo_area_tel: tel.codigo_area_tel ?? "",
      numero_tel: tel.numero_tel ?? "",
      observaciones_tel: tel.observaciones_tel ?? "",
    });
    setModalTelOpen(true);
  };

  const guardarTel = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formTel.tipo_tel || !formTel.codigo_area_tel || !formTel.numero_tel) return;
    setGuardandoTel(true);
    const payload = { ...formTel, observaciones_tel: formTel.observaciones_tel || null };
    try {
      if (editTelId == null) {
        await api.post(`/entidades/${matricula}/telefonos`, payload);
        toast.success("Teléfono creado.");
      } else {
        await api.patch(`/entidades/${matricula}/telefonos/${editTelId}`, payload);
        toast.success("Teléfono actualizado.");
      }
      setModalTelOpen(false);
      cargar();
    } catch {
      toast.error("No se pudo guardar el teléfono.");
    } finally {
      setGuardandoTel(false);
    }
  };

  const confirmarBajaTel = async () => {
    if (!aDarBajaTel) return;
    try {
      await api.patch(`/entidades/${matricula}/telefonos/${aDarBajaTel.id_tel}/baja`);
      toast.success("Teléfono dado de baja.");
      cargar();
    } catch {
      toast.error("No se pudo dar de baja el teléfono.");
    } finally {
      setABajaTel(null);
    }
  };

  const reactivarTelefono = async (t: TelefonoOut) => {
    try {
      await api.patch(`/entidades/${matricula}/telefonos/${t.id_tel}/reactivar`);
      toast.success("Teléfono reactivado.");
      cargar();
    } catch {
      toast.error("No se pudo reactivar el teléfono.");
    }
  };

  const confirmarBajaDir = async () => {
    if (!aDarBajaDir) return;
    try {
      await api.patch(`/entidades/${matricula}/direcciones/${aDarBajaDir.id_dir}/baja`);
      toast.success("Domicilio dado de baja.");
      cargar();
    } catch {
      toast.error("No se pudo dar de baja el domicilio.");
    } finally {
      setABajaDir(null);
    }
  };

  const reactivarDireccion = async (d: DireccionOut) => {
    try {
      await api.patch(`/entidades/${matricula}/direcciones/${d.id_dir}/reactivar`);
      toast.success("Domicilio reactivado.");
      cargar();
    } catch {
      toast.error("No se pudo reactivar el domicilio.");
    }
  };

  const abrirAltaDir = () => {
    setEditDirId(null);
    setFormDir(FORM_DIR_VACIO);
    setModalDirOpen(true);
  };

  const abrirEdicionDir = (dir: DireccionOut) => {
    setEditDirId(dir.id_dir);
    setFormDir({
      calle_dir: dir.calle_dir ?? "",
      nro_dir: dir.nro_dir ?? "",
      piso_dir: dir.piso_dir ?? "",
      dpto_dir: dir.dpto_dir ?? "",
      barrio_dir: dir.barrio_dir ?? "",
      cp_dir: dir.cp_dir ?? "",
      localidad_dir: dir.localidad_dir ?? "",
      departamento_dir: dir.departamento_dir ?? "",
      provincia_dir: dir.provincia_dir ?? "",
      tipo_dir: dir.tipo_dir ?? "",
      observacion_dir: dir.observacion_dir ?? "",
    });
    setModalDirOpen(true);
  };

  const guardarDir = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDir.calle_dir || !formDir.nro_dir || !formDir.barrio_dir || !formDir.cp_dir || !formDir.localidad_dir || !formDir.provincia_dir || !formDir.tipo_dir) return;
    setGuardandoDir(true);
    const payload = {
      ...formDir,
      piso_dir: formDir.piso_dir || null,
      dpto_dir: formDir.dpto_dir || null,
      departamento_dir: formDir.departamento_dir || null,
      observacion_dir: formDir.observacion_dir || null,
    };
    try {
      if (editDirId == null) {
        await api.post(`/entidades/${matricula}/direcciones`, payload);
        toast.success("Domicilio creado.");
      } else {
        await api.patch(`/entidades/${matricula}/direcciones/${editDirId}`, payload);
        toast.success("Domicilio actualizado.");
      }
      setModalDirOpen(false);
      cargar();
    } catch {
      toast.error("No se pudo guardar el domicilio.");
    } finally {
      setGuardandoDir(false);
    }
  };

  const abrirAltaMail = () => {
    setEditMailId(null);
    setFormMail(FORM_MAIL_VACIO);
    setModalMailOpen(true);
  };

  const abrirEdicionMail = (mail: MailAbmOut) => {
    setEditMailId(mail.id_mails);
    setFormMail({
      mail: mail.mail ?? "",
      tipo_mail: mail.tipo_mail ?? "",
    });
    setModalMailOpen(true);
  };

  const guardarMail = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formMail.mail || !formMail.tipo_mail) return;
    setGuardandoMail(true);
    try {
      if (editMailId == null) {
        await api.post(`/entidades/${matricula}/mails`, formMail);
        toast.success("Email creado.");
      } else {
        await api.patch(`/entidades/${matricula}/mails/${editMailId}`, formMail);
        toast.success("Email actualizado.");
      }
      setModalMailOpen(false);
      cargar();
    } catch {
      toast.error("No se pudo guardar el email.");
    } finally {
      setGuardandoMail(false);
    }
  };

  const confirmarBajaMail = async () => {
    if (!aDarBajaMail) return;
    try {
      await api.patch(`/entidades/${matricula}/mails/${aDarBajaMail.id_mails}/baja`);
      toast.success("Email dado de baja.");
      cargar();
    } catch {
      toast.error("No se pudo dar de baja el email.");
    } finally {
      setABajaMail(null);
    }
  };

  const reactivarMail = async (m: MailAbmOut) => {
    try {
      await api.patch(`/entidades/${matricula}/mails/${m.id_mails}/reactivar`);
      toast.success("Email reactivado.");
      cargar();
    } catch {
      toast.error("No se pudo reactivar el email.");
    }
  };

  if (!matricula) {
    return <p className="text-sm text-[var(--color-ink-soft)]">Buscá una cuenta para ver sus teléfonos y domicilios.</p>;
  }

  const telsActivos = telefonos.filter((t) => t.activo_tel === "S").length;
  const dirsActivos = direcciones.filter((d) => d.activa_dir === "S").length;

  return (
    <div className="space-y-6 animate-in">
      <div>
        <div className="flex items-center justify-between gap-2 flex-wrap mb-4">
          <h2 className="section-title">
            <i className="fas fa-phone" /> Teléfonos
          </h2>
          <button type="button" className="btn btn-secondary btn-sm" onClick={abrirAltaTel}>
            <i className="fas fa-plus" /> Nuevo teléfono
          </button>
        </div>

        {!loading && telefonos.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
            <StatCard label="Activos" value={telsActivos} icon="fa-phone" tone="success" />
            <StatCard label="Total" value={telefonos.length} icon="fa-phone" tone="brand" />
          </div>
        )}

        {loading ? (
          <TableSkeleton rows={5} cols={4} />
        ) : telefonos.length === 0 ? (
          <EmptyState icon="fa-phone-slash" title="Sin teléfonos" hint="No hay teléfonos registrados para esta cuenta." />
        ) : (
          <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
            <table className="data-table w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-[var(--color-ink-soft)] border-b border-[var(--color-line)]">
                  <th className="py-1.5">Tipo</th>
                  <th>Número</th>
                  <th>Estado</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {telefonos.map((t) => (
                  <tr key={t.id_tel} className="border-b border-[var(--color-line)]">
                    <td className="py-1.5">{t.tipo_tel ?? "—"}</td>
                    <td className="font-data">
                      {t.codigo_area_tel ? `(${t.codigo_area_tel}) ` : ""}
                      {t.numero_tel ?? "—"}
                    </td>
                    <td><FlagBadge value={t.activo_tel} labels={["Activo", "De baja"]} tones={["success", "neutral"]} /></td>
                    <td className="text-right whitespace-nowrap">
                      <button type="button" className="btn btn-ghost btn-sm" onClick={() => abrirEdicionTel(t)}>
                        <i className="fas fa-pen" /> Editar
                      </button>
                      {t.activo_tel === "S" ? (
                        <button
                          type="button"
                          className="btn btn-ghost-danger btn-sm"
                          onClick={() => setABajaTel(t)}
                        >
                          <i className="fas fa-trash" /> Dar de baja
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="btn btn-ghost btn-sm !text-[var(--color-success)]"
                          onClick={() => reactivarTelefono(t)}
                        >
                          <i className="fas fa-rotate-left" /> Reactivar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div>
        <div className="flex items-center justify-between gap-2 flex-wrap mb-4">
          <h2 className="section-title">
            <i className="fas fa-home" /> Domicilios
          </h2>
          <button type="button" className="btn btn-secondary btn-sm" onClick={abrirAltaDir}>
            <i className="fas fa-plus" /> Nuevo domicilio
          </button>
        </div>

        {!loading && direcciones.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
            <StatCard label="Activos" value={dirsActivos} icon="fa-home" tone="success" />
            <StatCard label="Total" value={direcciones.length} icon="fa-home" tone="brand" />
          </div>
        )}

        {loading ? (
          <TableSkeleton rows={5} cols={5} />
        ) : direcciones.length === 0 ? (
          <EmptyState icon="fa-map-marker-alt" title="Sin domicilios" hint="No hay domicilios registrados para esta cuenta." />
        ) : (
          <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
            <table className="data-table w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-[var(--color-ink-soft)] border-b border-[var(--color-line)]">
                  <th className="py-1.5">Domicilio</th>
                  <th>Localidad</th>
                  <th>Provincia</th>
                  <th>Estado</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {direcciones.map((d) => (
                  <tr key={d.id_dir} className="border-b border-[var(--color-line)]">
                    <td className="py-1.5">
                      {d.calle_dir ?? "—"} {d.nro_dir ?? ""}
                      {d.barrio_dir ? `, ${d.barrio_dir}` : ""}
                    </td>
                    <td>{d.localidad_dir ?? "—"}</td>
                    <td>{d.provincia_dir ?? "—"}</td>
                    <td><FlagBadge value={d.activa_dir} labels={["Activo", "De baja"]} tones={["success", "neutral"]} /></td>
                    <td className="text-right whitespace-nowrap">
                      <button type="button" className="btn btn-ghost btn-sm" onClick={() => abrirEdicionDir(d)}>
                        <i className="fas fa-pen" /> Editar
                      </button>
                      {d.activa_dir === "S" ? (
                        <button
                          type="button"
                          className="btn btn-ghost-danger btn-sm"
                          onClick={() => setABajaDir(d)}
                        >
                          <i className="fas fa-trash" /> Dar de baja
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="btn btn-ghost btn-sm !text-[var(--color-success)]"
                          onClick={() => reactivarDireccion(d)}
                        >
                          <i className="fas fa-rotate-left" /> Reactivar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal
        open={modalTelOpen}
        onClose={() => setModalTelOpen(false)}
        title={editTelId == null ? "Nuevo teléfono" : "Editar teléfono"}
        icon="fa-phone"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalTelOpen(false)}>Cancelar</button>
            <button type="submit" form="form-tel" className="btn btn-success" disabled={guardandoTel}>
              {guardandoTel ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-tel" onSubmit={guardarTel} className="space-y-3">
          <div>
            <label className="form-label">Tipo</label>
            <input
              type="text"
              value={formTel.tipo_tel}
              onChange={(e) => setFormTel({ ...formTel, tipo_tel: e.target.value })}
              className="form-input"
              required
              autoFocus
            />
          </div>
          <div>
            <label className="form-label">Código de área</label>
            <input
              type="tel"
              inputMode="numeric"
              pattern="\d{2,5}"
              title="Solo dígitos (2 a 5)"
              value={formTel.codigo_area_tel}
              onChange={(e) => setFormTel({ ...formTel, codigo_area_tel: e.target.value.replace(/\D/g, "") })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Número</label>
            <input
              type="tel"
              inputMode="numeric"
              pattern="\d{5,10}"
              title="Solo dígitos (5 a 10)"
              value={formTel.numero_tel}
              onChange={(e) => setFormTel({ ...formTel, numero_tel: e.target.value.replace(/\D/g, "") })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">Observaciones</label>
            <input
              type="text"
              value={formTel.observaciones_tel}
              onChange={(e) => setFormTel({ ...formTel, observaciones_tel: e.target.value })}
              className="form-input"
            />
          </div>
        </form>
      </Modal>

      <ConfirmDialog
        open={aDarBajaTel != null}
        title="Dar de baja teléfono"
        message={`¿Dar de baja el teléfono ${aDarBajaTel?.codigo_area_tel ? `(${aDarBajaTel.codigo_area_tel}) ` : ""}${aDarBajaTel?.numero_tel ?? ""}?`}
        confirmLabel="Dar de baja"
        onConfirm={confirmarBajaTel}
        onCancel={() => setABajaTel(null)}
      />

      <Modal
        open={modalDirOpen}
        onClose={() => setModalDirOpen(false)}
        title={editDirId == null ? "Nuevo domicilio" : "Editar domicilio"}
        icon="fa-home"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalDirOpen(false)}>Cancelar</button>
            <button type="submit" form="form-dir" className="btn btn-success" disabled={guardandoDir}>
              {guardandoDir ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-dir" onSubmit={guardarDir} className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="form-label">Calle*</label>
              <input
                type="text"
                value={formDir.calle_dir}
                onChange={(e) => setFormDir({ ...formDir, calle_dir: e.target.value })}
                className="form-input"
                required
                autoFocus
              />
            </div>
            <div>
              <label className="form-label">Nro*</label>
              <input
                type="text"
                value={formDir.nro_dir}
                onChange={(e) => setFormDir({ ...formDir, nro_dir: e.target.value })}
                className="form-input"
                required
              />
            </div>
            <div>
              <label className="form-label">Piso</label>
              <input
                type="text"
                value={formDir.piso_dir}
                onChange={(e) => setFormDir({ ...formDir, piso_dir: e.target.value })}
                className="form-input"
              />
            </div>
            <div>
              <label className="form-label">Dpto</label>
              <input
                type="text"
                value={formDir.dpto_dir}
                onChange={(e) => setFormDir({ ...formDir, dpto_dir: e.target.value })}
                className="form-input"
              />
            </div>
            <div>
              <label className="form-label">Barrio*</label>
              <input
                type="text"
                value={formDir.barrio_dir}
                onChange={(e) => setFormDir({ ...formDir, barrio_dir: e.target.value })}
                className="form-input"
                required
              />
            </div>
            <div>
              <label className="form-label">CP*</label>
              <input
                type="text"
                value={formDir.cp_dir}
                onChange={(e) => setFormDir({ ...formDir, cp_dir: e.target.value })}
                className="form-input"
                required
              />
            </div>
            <div>
              <label className="form-label">Localidad*</label>
              <input
                type="text"
                value={formDir.localidad_dir}
                onChange={(e) => setFormDir({ ...formDir, localidad_dir: e.target.value })}
                className="form-input"
                required
              />
            </div>
            <div>
              <label className="form-label">Departamento</label>
              <input
                type="text"
                value={formDir.departamento_dir}
                onChange={(e) => setFormDir({ ...formDir, departamento_dir: e.target.value })}
                className="form-input"
              />
            </div>
            <div>
              <label className="form-label">Provincia*</label>
              <select
                value={formDir.provincia_dir}
                onChange={(e) => setFormDir({ ...formDir, provincia_dir: e.target.value })}
                className="form-select"
                required
              >
                <option value="" disabled>Seleccionar provincia...</option>
                {PROVINCIAS.map((p) => (
                  <option key={p} value={p}>{p}</option>
                ))}
                {/* Valor legado que no coincide con el catálogo: se conserva para no romper la edición */}
                {formDir.provincia_dir && !PROVINCIAS.includes(formDir.provincia_dir) && (
                  <option value={formDir.provincia_dir}>{formDir.provincia_dir}</option>
                )}
              </select>
            </div>
            <div>
              <label className="form-label">Tipo*</label>
              <input
                type="text"
                value={formDir.tipo_dir}
                onChange={(e) => setFormDir({ ...formDir, tipo_dir: e.target.value })}
                className="form-input"
                required
              />
            </div>
          </div>
          <div>
            <label className="form-label">Observación</label>
            <input
              type="text"
              value={formDir.observacion_dir}
              onChange={(e) => setFormDir({ ...formDir, observacion_dir: e.target.value })}
              className="form-input"
            />
          </div>
        </form>
      </Modal>

      <ConfirmDialog
        open={aDarBajaDir != null}
        title="Dar de baja domicilio"
        message={`¿Dar de baja el domicilio ${aDarBajaDir?.calle_dir ?? ""} ${aDarBajaDir?.nro_dir ?? ""}?`}
        confirmLabel="Dar de baja"
        onConfirm={confirmarBajaDir}
        onCancel={() => setABajaDir(null)}
      />

      <div>
        <div className="flex items-center justify-between gap-2 flex-wrap mb-4">
          <h2 className="section-title">
            <i className="fas fa-envelope" /> Mails
          </h2>
          <button type="button" className="btn btn-secondary btn-sm" onClick={abrirAltaMail}>
            <i className="fas fa-plus" /> Nuevo mail
          </button>
        </div>

        {!loading && mails.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
            <StatCard label="Activos" value={mails.filter((m) => m.activo_mail === "S").length} icon="fa-envelope" tone="success" />
            <StatCard label="Total" value={mails.length} icon="fa-envelope" tone="brand" />
          </div>
        )}

        {loading ? (
          <TableSkeleton rows={5} cols={4} />
        ) : mails.length === 0 ? (
          <EmptyState icon="fa-envelope-open" title="Sin mails" hint="No hay mails registrados para esta cuenta." />
        ) : (
          <div className="overflow-x-auto rounded-lg border border-[var(--color-line)]">
            <table className="data-table w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-[var(--color-ink-soft)] border-b border-[var(--color-line)]">
                  <th className="py-1.5">Mail</th>
                  <th>Tipo</th>
                  <th>Estado</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {mails.map((m) => (
                  <tr key={m.id_mails} className="border-b border-[var(--color-line)]">
                    <td className="py-1.5 font-data">{m.mail ?? "—"}</td>
                    <td>{m.tipo_mail ?? "—"}</td>
                    <td><FlagBadge value={m.activo_mail} labels={["Activo", "De baja"]} tones={["success", "neutral"]} /></td>
                    <td className="text-right whitespace-nowrap">
                      <button type="button" className="btn btn-ghost btn-sm" onClick={() => abrirEdicionMail(m)}>
                        <i className="fas fa-pen" /> Editar
                      </button>
                      {m.activo_mail === "S" ? (
                        <button
                          type="button"
                          className="btn btn-ghost-danger btn-sm"
                          onClick={() => setABajaMail(m)}
                        >
                          <i className="fas fa-trash" /> Dar de baja
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="btn btn-ghost btn-sm !text-[var(--color-success)]"
                          onClick={() => reactivarMail(m)}
                        >
                          <i className="fas fa-rotate-left" /> Reactivar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <Modal
        open={modalMailOpen}
        onClose={() => setModalMailOpen(false)}
        title={editMailId == null ? "Nuevo mail" : "Editar mail"}
        icon="fa-envelope"
        footer={
          <>
            <button type="button" className="btn btn-secondary" onClick={() => setModalMailOpen(false)}>Cancelar</button>
            <button type="submit" form="form-mail" className="btn btn-success" disabled={guardandoMail}>
              {guardandoMail ? <><i className="fas fa-circle-notch fa-spin" /> Guardando...</> : <><i className="fas fa-check" /> Guardar</>}
            </button>
          </>
        }
      >
        <form id="form-mail" onSubmit={guardarMail} className="space-y-3">
          <div>
            <label className="form-label">Mail</label>
            <input
              type="email"
              value={formMail.mail}
              onChange={(e) => setFormMail({ ...formMail, mail: e.target.value })}
              className="form-input"
              required
              autoFocus
            />
          </div>
          <div>
            <label className="form-label">Tipo</label>
            <input
              type="text"
              value={formMail.tipo_mail}
              onChange={(e) => setFormMail({ ...formMail, tipo_mail: e.target.value })}
              className="form-input"
              required
            />
          </div>
        </form>
      </Modal>

      <ConfirmDialog
        open={aDarBajaMail != null}
        title="Dar de baja mail"
        message={`¿Dar de baja el mail ${aDarBajaMail?.mail ?? ""}?`}
        confirmLabel="Dar de baja"
        onConfirm={confirmarBajaMail}
        onCancel={() => setABajaMail(null)}
      />
    </div>
  );
}
