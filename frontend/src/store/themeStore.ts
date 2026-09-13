import { create } from "zustand";

type Theme = "light" | "dark";

function leerTemaInicial(): Theme {
  const guardado = localStorage.getItem("theme");
  if (guardado === "dark" || guardado === "light") return guardado;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function aplicar(theme: Theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
  localStorage.setItem("theme", theme);
}

interface ThemeState {
  theme: Theme;
  toggle: () => void;
}

export const useThemeStore = create<ThemeState>((set, get) => {
  const inicial = leerTemaInicial();
  aplicar(inicial);
  return {
    theme: inicial,
    toggle: () => {
      const next: Theme = get().theme === "dark" ? "light" : "dark";
      aplicar(next);
      set({ theme: next });
    },
  };
});
