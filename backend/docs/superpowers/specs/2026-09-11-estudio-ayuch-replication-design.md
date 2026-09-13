# Design Spec: Estudio Ayuch Replication

**Date:** 2026-09-11
**Status:** Approved
**Source Project:** vps-dw-backend-estudio_lg / vps-dw-frontend-estudio_lg

## Overview
Replicate the 'Estudio LG' project into 'Estudio Ayuch', implementing only a subset of modules and removing all functionality related to 'Acciones' and 'Resultados'.

## Scope

### Included Modules
- **Cargas Masivas**: Bulk data import.
- **Datos de la Cuenta**: Account details.
- **Teléfonos y Domicilios**: Contact phone and address management.
- **Contactos**: General contact management.
- **Informes de Contacto**: Contact reporting.
- **Configuración**: System settings (without actions/results).

### Excluded Modules
- All other modules not listed above (e.g., Judicial, Cobros, etc.).

### Hard Exclusions
- **Acciones y Resultados**: Total removal of any logic, endpoints, UI components, or database references to actions and results.

## Technical Design

### Backend (`vps-dw-backend-estudio_ayuch`)
- **Core**: Copy all of `src/core/` (DB, Security, etc.).
- **Models**: Copy all of `src/models/`.
- **API Entry**: Copy `src/api/main.py`.
- **Routers to Copy**:
    - `src/routers/carga_masiva.py`
    - `src/routers/cuentas.py`
    - `src/routers/informe_telefonos.py`
    - `src/routers/contactos_gestion.py`
    - `src/routers/informe_contactos.py`
    - `src/routers/config_catalogos.py`
    - `src/routers/perfiles.py`
    - `src/routers/usuarios.py`
- **Purge**:
    - Delete `src/routers/informe_ctas_acciones.py`.
    - Remove routes for actions/results from `src/api/main.py`.
    - Remove action/result endpoints from `src/routers/contactos_gestion.py`.

### Frontend (`vps-dw-frontend-estudio_ayuch`)
- **Infra**: Copy `src/api/`, `src/lib/`, `src/store/`, `src/types/`.
- **UI Base**: Copy `src/layout/`, `src/components/ui/`.
- **Pages/Sections to Copy**:
    - `src/pages/sections/CargaMasivaTab.tsx`
    - `src/pages/sections/DatosCuenta.tsx`
    - `src/pages/sections/TelefonosDomicilios.tsx`
    - `src/pages/sections/InformeTelefonos.tsx`
    - `src/pages/sections/Contactos.tsx`
    - `src/pages/sections/InformeContactos.tsx`
- **Config**: Copy `src/components/config/ConfiguracionModal.tsx` and related tabs.
- **Purge**:
    - Delete `src/pages/sections/InformeCuentasAcciones.tsx`.
    - Remove action/result UI (buttons, tables) from `Contactos.tsx` and `ConfiguracionModal.tsx`.
    - Remove action/result routes from `src/routes/navConfig.ts`.

### Infrastructure & Database
- **Docker**: Copy `Dockerfile`, `docker-compose.yml`, `requirements.txt`.
- **DB Init**: Copy `docker/init/*.sql`.
- **Migrations**: Copy `database/migrations/*.sql`.
- **Schema**: Copy `database/whatsapp_bot_estudio_lg.sql` and rename to `whatsapp_bot_estudio_ayuch.sql`.
- **Environment**: Update DB names in configuration to refer to 'estudio_ayuch'.

## Success Criteria
1. Application boots without errors in Docker.
2. Requested modules are accessible and functional.
3. No references to "Acciones" or "Resultados" exist in the UI or API.
4. Database schema is correctly initialized for Ayuch.
