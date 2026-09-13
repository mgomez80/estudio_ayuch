from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from src.core.database import engine
from src.routers import (
    cuentas, auth,
    informe_telefonos, informe_contactos,
    contactos_gestion,
    carga_masiva, usuarios, perfiles, config_catalogos,
)

app = FastAPI(
    title="Backend API - Estudio Ayuch",
    version="0.3.0",
    description="API interna para gestión de cuentas y contactos de Estudio Ayuch.",
)

# En dev, el frontend corre en otro puerto (ej. localhost:5173) -> hace falta CORS.
# En producción con el proxy de nginx (/api same-origin) esto no se usa, pero no molesta dejarlo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restringir a tu dominio real antes de ir a producción
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cuentas.router)
app.include_router(auth.router)
app.include_router(informe_telefonos.router)
app.include_router(informe_contactos.router)
app.include_router(contactos_gestion.router)
app.include_router(carga_masiva.router)
app.include_router(usuarios.router)
app.include_router(perfiles.router)
app.include_router(config_catalogos.router)

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
