import type { ReactNode } from "react";

export type BadgeTone =
  | "neutral"
  | "success"
  | "danger"
  | "warning"
  | "info"
  | "brand"
  | "judicial";

export function Badge({ tone = "neutral", children }: { tone?: BadgeTone; children: ReactNode }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

/** Badge para un flag "S"/"N" (activo, judicial, pagado, rendido, etc.). */
export function FlagBadge({
  value,
  labels = ["Sí", "No"],
  tones = ["success", "neutral"],
}: {
  value: string | null | undefined;
  labels?: [string, string];
  tones?: [BadgeTone, BadgeTone];
}) {
  const si = value === "S";
  return <Badge tone={si ? tones[0] : tones[1]}>{si ? labels[0] : labels[1]}</Badge>;
}
