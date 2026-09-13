import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Usuario } from "../types/domain";

interface AuthState {
  token: string | null;
  usuario: Usuario | null;
  setSession: (token: string, usuario: Usuario) => void;
  logout: () => void;
}

// TODO: confirmar contrato real del endpoint de login en backend-api
// (asumo POST /auth/login -> { access_token, usuario }). Ajustar cuando
// confirmes el esquema JWT que armaste en FastAPI.
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      usuario: null,
      setSession: (token, usuario) => set({ token, usuario }),
      logout: () => set({ token: null, usuario: null }),
    }),
    { name: "cobranza-auth" }
  )
);
