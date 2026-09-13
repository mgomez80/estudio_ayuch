from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from src.core.database import get_db
from src.core.security import get_current_admin
from src.models.catalogos import Modulo, Perfil, PerfilPermiso

router = APIRouter(prefix="/config", tags=["Configuración"])


# ============== Pydantic Models ==============

class ModuloOut(BaseModel):
    id_modulo: int
    clave: str
    desc_modulo: str

    class Config:
        from_attributes = True


class PermisoItem(BaseModel):
    modulos_id_modulo: int
    clave_modulo: str
    ver: str
    alta: str
    baja: str
    modificar: str


class PerfilOut(BaseModel):
    id_perfil: int
    nombre: str
    activo: str

    class Config:
        from_attributes = True


class PerfilDetailOut(BaseModel):
    id_perfil: int
    nombre: str
    activo: str
    permisos: List[PermisoItem]


class PerfilCreateRequest(BaseModel):
    nombre: str


class PerfilUpdateRequest(BaseModel):
    nombre: str = None
    activo: str = None


class PermisoUpsertItem(BaseModel):
    modulos_id_modulo: int
    ver: str
    alta: str
    baja: str
    modificar: str


# ============== Endpoints ==============

@router.get("/modulos", response_model=List[ModuloOut], dependencies=[Depends(get_current_admin)])
def get_modulos(db: Session = Depends(get_db)):
    """Lista todos los módulos para armar la matriz de permisos en el frontend."""
    modulos = db.query(Modulo).all()
    return modulos


@router.get("/perfiles", response_model=List[PerfilOut], dependencies=[Depends(get_current_admin)])
def get_perfiles(db: Session = Depends(get_db)):
    """Lista todos los perfiles."""
    perfiles = db.query(Perfil).all()
    return perfiles


@router.get("/perfiles/{id_perfil}", response_model=PerfilDetailOut, dependencies=[Depends(get_current_admin)])
def get_perfil_detail(id_perfil: int, db: Session = Depends(get_db)):
    """Obtiene un perfil con su matriz de permisos actual.

    Devuelve: {id_perfil, nombre, activo, permisos: [{modulos_id_modulo, clave_modulo, ver, alta, baja, modificar}, ...]}
    """
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    # Join con módulos para obtener la clave
    permisos_raw = db.query(
        PerfilPermiso.modulos_id_modulo,
        Modulo.clave,
        PerfilPermiso.ver,
        PerfilPermiso.alta,
        PerfilPermiso.baja,
        PerfilPermiso.modificar,
    ).join(
        Modulo, PerfilPermiso.modulos_id_modulo == Modulo.id_modulo
    ).filter(
        PerfilPermiso.perfiles_id_perfil == id_perfil
    ).all()

    permisos = [
        PermisoItem(
            modulos_id_modulo=row.modulos_id_modulo,
            clave_modulo=row.clave,
            ver=row.ver,
            alta=row.alta,
            baja=row.baja,
            modificar=row.modificar,
        )
        for row in permisos_raw
    ]

    return PerfilDetailOut(
        id_perfil=perfil.id_perfil,
        nombre=perfil.nombre,
        activo=perfil.activo,
        permisos=permisos,
    )


@router.post("/perfiles", response_model=PerfilOut, dependencies=[Depends(get_current_admin)])
def create_perfil(payload: PerfilCreateRequest, db: Session = Depends(get_db)):
    """Crea un perfil sin permisos (se asignan luego con PUT /perfiles/{id}/permisos)."""
    perfil = Perfil(nombre=payload.nombre, activo="S")
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


@router.patch("/perfiles/{id_perfil}", response_model=PerfilOut, dependencies=[Depends(get_current_admin)])
def update_perfil(id_perfil: int, payload: PerfilUpdateRequest, db: Session = Depends(get_db)):
    """Edita nombre y/o estado (activo) de un perfil."""
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    if payload.nombre is not None:
        perfil.nombre = payload.nombre
    if payload.activo is not None:
        perfil.activo = payload.activo

    db.commit()
    db.refresh(perfil)
    return perfil


@router.put("/perfiles/{id_perfil}/permisos", dependencies=[Depends(get_current_admin)])
def upsert_perfil_permisos(id_perfil: int, payload: List[PermisoUpsertItem], db: Session = Depends(get_db)):
    """Reemplaza la matriz completa de permisos de un perfil en una transacción.

    Body: [{modulos_id_modulo, ver, alta, baja, modificar}, ...]

    Implementación: DELETE + bulk INSERT en la misma sesión (rollback si falla).
    """
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    try:
        # Eliminar permisos existentes
        db.query(PerfilPermiso).filter(
            PerfilPermiso.perfiles_id_perfil == id_perfil
        ).delete(synchronize_session=False)

        # Insertar nuevos permisos
        for item in payload:
            permiso = PerfilPermiso(
                perfiles_id_perfil=id_perfil,
                modulos_id_modulo=item.modulos_id_modulo,
                ver=item.ver,
                alta=item.alta,
                baja=item.baja,
                modificar=item.modificar,
            )
            db.add(permiso)

        db.commit()
        return {"message": "Permisos actualizados correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar permisos: {str(e)}")


@router.delete("/perfiles/{id_perfil}", dependencies=[Depends(get_current_admin)])
def delete_perfil(id_perfil: int, db: Session = Depends(get_db)):
    """Soft-delete: marca el perfil como inactivo (activo = 'N')."""
    perfil = db.query(Perfil).filter(Perfil.id_perfil == id_perfil).first()
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")

    perfil.activo = "N"
    db.commit()
    return {"message": "Perfil desactivado correctamente"}
