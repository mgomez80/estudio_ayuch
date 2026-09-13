import { create } from "zustand";
import type { CuentaDetalleOut, CuentaOut } from "../types/domain";

interface AccountState {
  cuenta: CuentaDetalleOut | null;
  otrasCuentas: CuentaOut[];
  setCuenta: (cuenta: CuentaDetalleOut | null) => void;
  setOtrasCuentas: (cuentas: CuentaOut[]) => void;
}

export const useAccountStore = create<AccountState>((set) => ({
  cuenta: null,
  otrasCuentas: [],
  setCuenta: (cuenta) => set({ cuenta }),
  setOtrasCuentas: (otrasCuentas) => set({ otrasCuentas }),
}));
