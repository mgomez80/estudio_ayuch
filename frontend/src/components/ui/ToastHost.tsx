import { useToastStore, type ToastType } from "../../store/toastStore";

const CONF: Record<ToastType, { icon: string; cls: string }> = {
  success: { icon: "fa-circle-check", cls: "badge-success" },
  error: { icon: "fa-circle-exclamation", cls: "badge-danger" },
  info: { icon: "fa-circle-info", cls: "badge-info" },
};

/** Contenedor global de toasts (aria-live). Montar una vez en el layout. */
export function ToastHost() {
  const toasts = useToastStore((s) => s.toasts);
  const remove = useToastStore((s) => s.remove);

  return (
    <div className="fixed bottom-4 right-4 z-[60] flex flex-col gap-2 w-80 max-w-[calc(100vw-2rem)]" aria-live="polite" aria-atomic="false">
      {toasts.map((t) => {
        const c = CONF[t.type];
        return (
          <div
            key={t.id}
            role="status"
            className="card px-4 py-3 flex items-start gap-3 animate-in shadow-[var(--shadow-pop)]"
          >
            <span className={`badge ${c.cls} !rounded-lg !px-1.5 !py-1 mt-0.5`}>
              <i className={`fas ${c.icon}`} />
            </span>
            <p className="text-sm flex-1 text-[var(--color-ink)]">{t.message}</p>
            <button
              type="button"
              onClick={() => remove(t.id)}
              aria-label="Cerrar"
              className="text-[var(--color-ink-soft)] hover:text-[var(--color-ink)] transition-colors"
            >
              <i className="fas fa-xmark" />
            </button>
          </div>
        );
      })}
    </div>
  );
}
