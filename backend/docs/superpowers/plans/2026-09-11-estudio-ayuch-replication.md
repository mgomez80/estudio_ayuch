# Estudio Ayuch Replication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replicate 'estudio lg' project into 'Estudio Ayuch' with only selected modules and zero traces of 'Acciones' and 'Resultados'.

**Architecture:** Surgical copy of existing backend and frontend. selective migration of routers and components from the source project to a new target directory structure.

**Tech Stack:** Python (FastAPI), React (TypeScript), Docker, MySQL.

## Global Constraints
- Source Backend: `/home/soporte/proyectos/vps-dw-backend-estudio_lg`
- Target Backend: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch`
- Source Frontend: `/home/soporte/proyectos/vps-dw-frontend-estudio_lg`
- Target Frontend: `/home/soporte/proyectos/vps-dw-frontend-estudio_ayuch`
- Exclude ALL logic/UI related to "Acciones" and "Resultados".
- Maintain exactly the same structure as source for the copied files.

---

### Task 1: Infrastructure & Database Scaffolding

**Files:**
- Create: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch/Dockerfile`
- Create: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch/docker-compose.yml`
- Create: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch/requirements.txt`
- Create: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch/docker/init/` (all .sql files)
- Create: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch/database/migrations/` (all .sql files)
- Create: `/home/soporte/proyectos/vps-dw-backend-estudio_ayuch/database/whatsapp_bot_estudio_ayuch.sql`

- [ ] **Step 1: Create directory structure**
  ```bash
  mkdir -p /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/{docker/init,database/migrations,src/{api,core,models,routers}}
  ```
- [ ] **Step 2: Copy Docker and dependency files**
  ```bash
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/Dockerfile /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/docker-compose.yml /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/requirements.txt /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/
  ```
- [ ] **Step 3: Copy DB initialization scripts**
  ```bash
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/docker/init/*.sql /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/docker/init/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/database/migrations/*.sql /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/database/migrations/
  ```
- [ ] **Step 4: Copy and rename main schema**
  ```bash
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/database/whatsapp_bot_estudio_lg.sql /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/database/whatsapp_bot_estudio_ayuch.sql
  ```
- [ ] **Step 5: Commit infra**
  ```bash
  # Assuming git is initialized in the target
  git add .
  git commit -m "infra: initial scaffolding for estudio ayuch"
  ```

### Task 2: Backend Core & Models

**Files:**
- Copy: `src/core/` (entirely)
- Copy: `src/models/` (entirely)

- [ ] **Step 1: Copy core logic**
  ```bash
  cp -r /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/core /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/
  ```
- [ ] **Step 2: Copy models**
  ```bash
  cp -r /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/models /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/
  ```
- [ ] **Step 3: Commit core**
  ```bash
  git add src/core src/models
  git commit -m "backend: copy core and models"
  ```

### Task 3: Backend Routers (Surgical Copy & Purge)

**Files:**
- Copy: `src/routers/carga_masiva.py`, `cuentas.py`, `informe_telefonos.py`, `contactos_gestion.py`, `informe_contactos.py`, `config_catalogos.py`, `perfiles.py`, `usuarios.py`
- Modify: `src/routers/contactos_gestion.py`

- [ ] **Step 1: Copy required routers**
  ```bash
  # Copy only the approved routers
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/carga_masiva.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/cuentas.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/informe_telefonos.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/contactos_gestion.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/informe_contactos.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/config_catalogos.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/perfiles.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/routers/usuarios.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/routers/
  ```
- [ ] **Step 2: Purge action/result endpoints from contactos_gestion.py**
  Identify and remove all routes related to `acciones` and `resultados` in `src/routers/contactos_gestion.py`.
- [ ] **Step 3: Commit routers**
  ```bash
  git add src/routers/
  git commit -m "backend: surgical copy of routers and purge of actions/results"
  ```

### Task 4: Backend API Integration

**Files:**
- Copy: `src/api/main.py`
- Modify: `src/api/main.py`

- [ ] **Step 1: Copy main API entry**
  ```bash
  cp /home/soporte/proyectos/vps-dw-backend-estudio_lg/src/api/main.py /home/soporte/proyectos/vps-dw-backend-estudio_ayuch/src/api/
  ```
- [ ] **Step 2: Purge action/result routes in main.py**
  Remove all `app.include_router(...)` calls related to `informe_ctas_acciones` and any other actions/results routers.
- [ ] **Step 3: Commit API**
  ```bash
  git add src/api/main.py
  git commit -m "backend: integrate API and remove excluded routers"
  ```

### Task 5: Frontend Infrastructure & Base UI

**Files:**
- Create: `/home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/`
- Copy: `src/api/`, `src/lib/`, `src/store/`, `src/types/`, `src/layout/`, `src/components/ui/`
- Copy: `package.json`, `tsconfig.json`, `vite.config.ts`, `index.html`, `Dockerfile`, `nginx.conf`

- [ ] **Step 1: Create folder structure**
  ```bash
  mkdir -p /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/{api,lib,store,types,layout,components/ui,pages/sections}
  ```
- [ ] **Step 2: Copy infra and base UI**
  ```bash
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/api /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/lib /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/store /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/types /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/layout /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/components/ui /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/components/
  ```
- [ ] **Step 3: Copy root config files**
  ```bash
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/package.json /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/tsconfig.json /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/vite.config.ts /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/index.html /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/Dockerfile /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/nginx.conf /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/
  ```
- [ ] **Step 4: Commit infra**
  ```bash
  git add .
  git commit -m "frontend: initial infra and base UI"
  ```

### Task 6: Frontend Pages & Sections (Surgical Copy & Purge)

**Files:**
- Copy: `src/pages/sections/CargaMasivaTab.tsx`, `DatosCuenta.tsx`, `TelefonosDomicilios.tsx`, `InformeTelefonos.tsx`, `Contactos.tsx`, `InformeContactos.tsx`
- Copy: `src/components/config/ConfiguracionModal.tsx` (and related tabs)
- Modify: `src/pages/sections/Contactos.tsx`, `src/components/config/ConfiguracionModal.tsx`

- [ ] **Step 1: Copy approved sections**
  ```bash
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/pages/sections/CargaMasivaTab.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/pages/sections/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/pages/sections/DatosCuenta.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/pages/sections/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/pages/sections/TelefonosDomicilios.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/pages/sections/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/pages/sections/InformeTelefonos.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/pages/sections/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/pages/sections/Contactos.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/pages/sections/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/pages/sections/InformeContactos.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/pages/sections/
  ```
- [ ] **Step 2: Copy config modal and related tabs**
  ```bash
  mkdir -p /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/components/config
  cp -r /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/components/config/* /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/components/config/
  ```
- [ ] **Step 3: Purge action/result UI**
  In `src/pages/sections/Contactos.tsx` and `src/components/config/ConfiguracionModal.tsx`, remove any components, buttons, or table columns referring to "Acciones" or "Resultados".
- [ ] **Step 4: Commit sections**
  ```bash
  git add src/pages/sections src/components/config
  git commit -m "frontend: surgical copy of sections and purge of actions/results"
  ```

### Task 7: Frontend Routes & Navigation

**Files:**
- Copy: `src/routes/navConfig.ts`
- Modify: `src/routes/navConfig.ts`
- Copy: `src/routes/ProtectedRoute.tsx`

- [ ] **Step 1: Copy routing files**
  ```bash
  mkdir -p /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/routes
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/routes/navConfig.ts /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/routes/
  cp /home/soporte/proyectos/vps-dw-frontend-estudio_lg/src/routes/ProtectedRoute.tsx /home/soporte/proyectos/vps-dw-frontend-estudio_ayuch/src/routes/
  ```
- [ ] **Step 2: Purge excluded routes**
  In `src/routes/navConfig.ts`, remove entries for `InformeCuentasAcciones` and any other excluded modules.
- [ ] **Step 3: Commit routes**
  ```bash
  git add src/routes/
  git commit -m "frontend: integrate navigation and remove excluded routes"
  ```

### Task 8: Final Integration & Verification

- [ ] **Step 1: Backend Verification**
  Run backend in Docker and check `GET /docs` to ensure only approved routers are present.
- [ ] **Step 2: Frontend Verification**
  Build and run frontend. Verify that only approved modules appear in the sidebar/navigation.
- [ ] **Step 3: End-to-End Smoke Test**
  Perform a basic flow: Login $\rightarrow$ Account Details $\rightarrow$ Contacts $\rightarrow$ Reports. Ensure no "Acciones" mentions appear.
- [ ] **Step 4: Final Commit**
  ```bash
  git add .
  git commit -m "chore: finalize replication of Estudio Ayuch"
  ```
