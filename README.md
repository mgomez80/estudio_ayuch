# Estudio Ayuch

Stack completo: FastAPI (backend) + React/Vite (frontend) + MySQL 8.

```
backend/    API FastAPI (puertos internos 8000)
frontend/   SPA React + nginx (puerto 80 interno)
docker-compose.yml   stack completo (db + api + frontend)
```

## Deploy en VPS

```bash
git clone git@github.com:mgomez80/estudio_ayuch.git
cd estudio_ayuch
cp .env.example .env
nano .env        # cambiar JWT_SECRET, credenciales DB y VITE_API_URL
docker compose up -d --build
```

Puertos: frontend **3008**, backend **8005** (solo localhost), MySQL **3312**.

### VITE_API_URL

La URL del backend queda embebida en el bundle del frontend al compilar.
Opciones:

- **Apache proxyeando `/api`** (recomendado): setear `VITE_API_URL=https://tu-dominio/api`
  y en el vhost:
  ```apache
  ProxyPass /api http://127.0.0.1:8005/
  ProxyPassReverse /api http://127.0.0.1:8005/
  ```
- **Directo por puerto**: `VITE_API_URL=http://IP-VPS:8005` y cambiar el publish
  del puerto api en `docker-compose.yml` a `"8005:8000"`.

### Notas

- El primer `docker compose up` crea las bases y el usuario desde
  `backend/docker/init/` y corre el seed (usuario `admin` / password `admin123` — cambiarla).
- Si el backend necesita hablar con `evolution_api`/n8n, agregar la red externa
  `agentes_net` al servicio `api` en `docker-compose.yml`.
- Cambiar `VITE_API_URL` requiere re-build del frontend (`docker compose up -d --build frontend`).