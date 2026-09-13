import { useEffect, type ReactNode } from "react";
import { createPortal } from "react-dom";

/** Modal accesible: overlay con blur, cierre por Escape / click en backdrop, header con título. */
export function Modal({
  open,
  onClose,
  title,
  icon,
  children,
  footer,
  size = "md",
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  icon?: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: "sm" | "md" | "lg";
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  const maxW = size === "sm" ? "max-w-md" : size === "lg" ? "max-w-3xl" : "max-w-xl";

  return createPortal(
    <div className="modal-overlay" onMouseDown={onClose} role="dialog" aria-modal="true" aria-label={title}>
      <div className={`modal-panel ${maxW}`} onMouseDown={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="section-title text-sm">
            {icon && <i className={`fas ${icon}`} />}
            {title}
          </h3>
          <button
            type="button"
            onClick={onClose}
            aria-label="Cerrar"
            className="btn btn-ghost btn-sm !px-2"
          >
            <i className="fas fa-xmark" />
          </button>
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>,
    document.body
  );
}
