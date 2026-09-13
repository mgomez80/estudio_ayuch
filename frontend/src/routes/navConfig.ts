// Fuente única de verdad para el sidebar. Cada entrada = un link del PHP original.
// path se resuelve as /cuenta/:id_cta/:seccion

export interface NavItem {
  seccion: string;
  label: string;
  icon: string; // clase font-awesome, se mantiene por continuidad visual con el sistema viejo
  implementado: boolean; // marca si ya está conectado a un endpoint real o es placeholder
  accent?: string; // variable CSS de color para el ícono (rompe la monotonía por grupo funcional)
  href?: string; // si viene seteado junto a externalBlank, el link es un <a> plano en vez de NavLink
  externalBlank?: boolean; // abre href en nueva pestaña
}

export const NAV_EXTRAJUDICIAL: NavItem[] = [
  { seccion: "datos", label: "Datos de la cuenta", icon: "fa-id-card", implementado: true, accent: "--color-brand" },
  { seccion: "teldom", label: "Teléfonos y Domicilios", icon: "fa-phone", implementado: true, accent: "--color-contact" },
  { seccion: "contactos", label: "Contactos", icon: "fa-address-book", implementado: true, accent: "--color-contact" },
  { seccion: "informe_de_telefonos", label: "Informe de Teléfonos", icon: "fa-phone-alt", implementado: true, accent: "--color-info" },
  { seccion: "informes_contactos", label: "Informes de Contactos", icon: "fa-users", implementado: true, accent: "--color-info" },
];
