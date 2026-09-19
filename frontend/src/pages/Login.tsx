import { useState, type FormEvent } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuthStore } from "../store/authStore";

export default function Login() {
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const setSession = useAuthStore((s) => s.setSession);
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      // TODO: confirmar el path/contrato real una vez definamos el endpoint de auth en FastAPI
      const { data } = await api.post("/auth/login", { usuario, password });
      setSession(data.access_token, data.usuario);
      navigate("/");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (err.response?.status === 401) {
          setError("Usuario o contraseña incorrectos.");
        } else if (err.response) {
          setError(`Error del servidor (${err.response.status}). Intentá de nuevo.`);
        } else {
          setError("No se pudo conectar con el servidor. Verificá la conexión o la URL de la API.");
        }
      } else {
        setError("Error inesperado. Intentá de nuevo.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-paper)] animate-in">
      <form
        onSubmit={handleSubmit}
        className="card w-full max-w-sm p-8"
      >
        <div className="flex flex-col items-center mb-6">
          <span className="grid place-items-center w-12 h-12 rounded-xl text-white bg-gradient-to-br from-[var(--color-brand)] to-[var(--color-brand-accent)] mb-3">
            <i className="fas fa-hand-holding-dollar" />
          </span>
          <h1 className="text-lg font-semibold text-[var(--color-ink)]">
            Seguimiento de Deudores
          </h1>
          <p className="text-sm text-[var(--color-ink-soft)] mt-1">Ingresá para continuar</p>
        </div>

        {error && (
          <div className="mb-4 text-sm rounded-md px-3 py-2 bg-[var(--color-danger-soft)] text-[var(--color-danger)]">
            {error}
          </div>
        )}

        <label className="form-label">Usuario</label>
        <input
          className="form-input mb-4"
          value={usuario}
          onChange={(e) => setUsuario(e.target.value)}
          autoFocus
        />

        <label className="form-label">Contraseña</label>
        <input
          type="password"
          className="form-input mb-6"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary w-full"
        >
          <i className="fas fa-sign-in-alt" /> {loading ? "Ingresando..." : "Ingresar"}
        </button>
      </form>
    </div>
  );
}
