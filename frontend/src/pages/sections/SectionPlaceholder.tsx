export default function SectionPlaceholder({ titulo, icon, hint }: { titulo: string; icon: string; hint?: string }) {
  return (
    <div className="text-center py-16">
      <i className={`fas ${icon} text-3xl text-[var(--color-line)] mb-3`} />
      <h2 className="text-sm font-semibold text-[var(--color-ink)]">{titulo}</h2>
      <p className="text-xs text-[var(--color-ink-soft)] mt-1 max-w-xs mx-auto">
        {hint ??
          "Falta el archivo PHP original o el endpoint del backend para esta sección. Pasámelo y la conecto."}
      </p>
    </div>
  );
}
