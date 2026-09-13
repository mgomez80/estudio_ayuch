import { EmptyState } from "../components/ui/EmptyState";

export default function BuscadorInicial() {
  return (
    <div className="animate-in">
      <EmptyState
        icon="fa-magnifying-glass-dollar"
        title="Buscá una cuenta para empezar"
        hint="Usá el buscador de arriba por número de cuenta, documento o razón social."
      />
    </div>
  );
}
