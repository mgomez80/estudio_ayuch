import { Component, type ReactNode } from "react";

/** Error boundary de sección: si una página tira, muestra fallback en vez de romper todo. */
export class ErrorBoundary extends Component<{ children: ReactNode }, { error: Error | null }> {
  state = { error: null as Error | null };

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div className="flex flex-col items-center justify-center text-center py-12 px-4">
          <div className="grid place-items-center w-14 h-14 rounded-2xl bg-[var(--color-danger-soft)] text-[var(--color-danger)] mb-3">
            <i className="fas fa-triangle-exclamation text-xl" />
          </div>
          <p className="text-sm font-semibold">Ocurrió un error al mostrar esta sección</p>
          <p className="text-xs text-[var(--color-ink-soft)] mt-1">{this.state.error.message}</p>
          <button className="btn btn-secondary mt-4" onClick={() => this.setState({ error: null })}>
            <i className="fas fa-rotate-right" /> Reintentar
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
