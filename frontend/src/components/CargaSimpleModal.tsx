import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { Modal } from "./ui/Modal";
import { toast } from "../store/toastStore";

interface SubclienteOpt {
  id_subcli: number;
  nombre_subcli: string;
}

const FORM_VACIO = {
  matricula: "",
  razon_social: "",
  id_subcli: 0,
  deudaact: "",
  cuenta_cliente: "",
  observacion: "",
};

/** Alta rápida de una cuenta: crea entidad + cuenta en un paso (botón "Carga simple"). */
export default function CargaSimpleModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [form, setForm] = useState(FORM_VACIO);
  const [subclientes, setSubclientes] = useState<SubclienteOpt[]>([]);
  const [guardando, setGuardando] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!open) return;
    setForm(FORM_VACIO);
    api
      .get<SubclienteOpt[]>("/catalogos/subclientes")
      .then(({ data }) => {
        setSubclientes(data);
        if (data.length === 1) setForm((f) => ({ ...f, id_subcli: data[0].id_subcli }));
      })
      .catch(() => setSubclientes([]));
  }, [open]);

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    setGuardando(true);
    try {
      const { data } = await api.post("/cuentas/alta-simple", {
        matricula: form.matricula,
        razon_social: form.razon_social,
        id_subcli: Number(form.id_subcli),
        deudaact: Number(form.deudaact),
        cuenta_cliente: form.cuenta_cliente || null,
        observacion: form.observacion || null,
      });
      toast.success(`Cuenta ${data.id_cta} creada`);
      onClose();
      navigate(`/cuenta/${data.id_cta}/datos`);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : "No se pudo crear la cuenta");
    } finally {
      setGuardando(false);
    }
  };

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Carga simple"
      icon="fa-user-plus"
      footer={
        <>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" form="form-carga-simple" className="btn btn-success" disabled={guardando}>
            {guardando ? "Creando..." : "Crear cuenta"}
          </button>
        </>
      }
    >
      <form id="form-carga-simple" onSubmit={guardar} className="space-y-3">
        <div>
          <label className="form-label">Documento / CUIT</label>
          <input
            type="text"
            inputMode="numeric"
            pattern="\d{6,30}"
            title="Solo dígitos (mínimo 6)"
            value={form.matricula}
            onChange={(e) => setForm({ ...form, matricula: e.target.value.replace(/\D/g, "") })}
            className="form-input"
            required
            autoFocus
          />
        </div>
        <div>
          <label className="form-label">Razón social / Nombre</label>
          <input
            type="text"
            minLength={3}
            maxLength={200}
            value={form.razon_social}
            onChange={(e) => setForm({ ...form, razon_social: e.target.value })}
            className="form-input"
            required
          />
        </div>
        <div>
          <label className="form-label">Subcliente</label>
          <select
            value={form.id_subcli}
            onChange={(e) => setForm({ ...form, id_subcli: Number(e.target.value) })}
            className="form-select"
            required
          >
            <option value={0} disabled>
              Seleccionar subcliente...
            </option>
            {subclientes.map((s) => (
              <option key={s.id_subcli} value={s.id_subcli}>
                {s.nombre_subcli}
              </option>
            ))}
          </select>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="form-label">Deuda inicial ($)</label>
            <input
              type="number"
              min={0}
              step="0.01"
              value={form.deudaact}
              onChange={(e) => setForm({ ...form, deudaact: e.target.value })}
              className="form-input"
              required
            />
          </div>
          <div>
            <label className="form-label">N° cuenta cliente (opcional)</label>
            <input
              type="text"
              maxLength={50}
              value={form.cuenta_cliente}
              onChange={(e) => setForm({ ...form, cuenta_cliente: e.target.value })}
              className="form-input"
            />
          </div>
        </div>
        <div>
          <label className="form-label">Observación (opcional)</label>
          <input
            type="text"
            maxLength={250}
            value={form.observacion}
            onChange={(e) => setForm({ ...form, observacion: e.target.value })}
            className="form-input"
          />
        </div>
      </form>
    </Modal>
  );
}
