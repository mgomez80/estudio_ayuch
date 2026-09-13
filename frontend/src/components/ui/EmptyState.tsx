/** Estado vacío: ícono + mensaje, opcionalmente una acción. */
export function EmptyState({
  icon = "fa-inbox",
  title,
  hint,
  action,
}: {
  icon?: string;
  title: string;
  hint?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-12 px-4 animate-in">
      <div
        className="grid place-items-center w-14 h-14 rounded-2xl mb-3"
        style={{
          backgroundImage:
            "linear-gradient(135deg, color-mix(in srgb, var(--st-accent, var(--color-brand)) 12%, var(--color-surface-2)), color-mix(in srgb, var(--st-accent, var(--color-brand)) 24%, var(--color-surface-2)))",
          color: "var(--st-accent, var(--color-brand))",
        }}
      >
        <i className={`fas ${icon} text-xl`} />
      </div>
      <p className="text-sm font-semibold text-[var(--color-ink)]">{title}</p>
      {hint && <p className="text-xs text-[var(--color-ink-soft)] mt-1 max-w-xs">{hint}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
