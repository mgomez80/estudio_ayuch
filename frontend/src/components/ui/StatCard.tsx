import type { BadgeTone } from "./Badge";

const ACCENT: Record<string, string> = {
  brand: "var(--color-brand)",
  success: "var(--color-success)",
  danger: "var(--color-danger)",
  warning: "var(--color-warning)",
  info: "var(--color-info)",
  judicial: "var(--color-judicial)",
  neutral: "var(--color-ink-soft)",
};

/** Tarjeta de resumen para encabezar informes/listados (conteos, totales). */
export function StatCard({
  label,
  value,
  icon,
  tone = "brand",
}: {
  label: string;
  value: React.ReactNode;
  icon?: string;
  tone?: BadgeTone;
}) {
  return (
    <div
      className="stat-card"
      style={{
        borderLeft: `3px solid ${ACCENT[tone]}`,
        backgroundImage: `linear-gradient(135deg, color-mix(in srgb, ${ACCENT[tone]} 8%, var(--color-surface-2)), var(--color-surface-2) 70%)`,
      }}
    >
      <span className="stat-label">
        {icon && <i className={`fas ${icon} mr-1`} style={{ color: ACCENT[tone] }} />}
        {label}
      </span>
      <span className="stat-value" style={{ color: ACCENT[tone] }}>
        {value}
      </span>
    </div>
  );
}
