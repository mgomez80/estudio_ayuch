from pathlib import Path

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from src.core.database import engine
from src.routers import (
    cuentas, auth,
    informe_telefonos, informe_contactos, informe_cuentas,
    contactos_gestion,
    carga_masiva, usuarios, perfiles, config_catalogos,
    cobros_abm, informe_cobros, entidades_abm, asistente,
)

app = FastAPI(
    title="Backend API - Estudio Ayuch",
    version="0.3.0",
    description="API interna para gestión de cuentas y contactos de Estudio Ayuch.",
)

# CORS restringido. En producción el frontend habla same-origin vía proxy
# nginx (/api), así que la lista suele quedar vacía o con el dominio real.
# Configurable por env: CORS_ORIGINS="https://midominio.com,https://www.midominio.com"
# Default: solo orígenes de desarrollo local (Vite).
_cors_origins_env = os.getenv("CORS_ORIGINS", "").strip()
_cors_origins = (
    [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    if _cors_origins_env
    else ["http://localhost:5173", "http://127.0.0.1:5173"]
)
if "*" in _cors_origins:
    raise RuntimeError(
        "CORS_ORIGINS no puede contener '*': esta API usa Authorization por header "
        "y un origen comodín expone todos los endpoints a cualquier sitio."
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=False,
    max_age=600,
)


# Security headers (best-practices: OWASP/Lighthouse). La API no sirve HTML,
# pero estos headers protegen también el /static y respuestas descargables.
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    response.headers.setdefault(
        "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
    )
    response.headers.setdefault(
        "Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'"
    )
    return response

app.include_router(cuentas.router)
app.include_router(auth.router)
app.include_router(informe_telefonos.router)
app.include_router(informe_contactos.router)
app.include_router(informe_cuentas.router)
app.include_router(contactos_gestion.router)
app.include_router(carga_masiva.router)
app.include_router(usuarios.router)
app.include_router(perfiles.router)
app.include_router(config_catalogos.router)
app.include_router(cobros_abm.router)
app.include_router(informe_cobros.router)
app.include_router(entidades_abm.router)
app.include_router(asistente.router)

# Adjuntos de WhatsApp (imágenes/docs subidos desde el panel) servidos como estáticos.
storage_dir = Path("storage")
storage_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=storage_dir), name="static")


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok"}


@app.get("/health/db", tags=["Sistema"])
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}
