"""
ABM de Cobros. Simplificado a propósito respecto del esquema legado:
- Sin vínculo a convenios/cuotas (eso queda para cuando se implemente Convenios).
- Concepto fijo a dos valores: CAPITAL y HONORARIOS (ver seed en
  backend/docker/init/05-conceptos-cobros.sql).
- Un cobro solo pide fecha, concepto, importe y si está rendido (S/N).
"""
from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.cuentas import Cuenta
from src.models.catalogos import Concepto
from src.models.financiero import Cobro, Movimiento

router = APIRouter(tags=["Cobros"])

# Los cobros no tienen concepto libre: solo estos dos, seedeados en la tabla
# `conceptos` bajo el rubro "Cobros" (ver 05-conceptos-cobros.sql).
CONCEPTOS_COBRO = ["CAPITAL", "HONORARIOS"]

# Etiqueta de fallback para cobros legados sin concepto propio (ej. vinculados
# a un convenio, esquema que este ABM ya no usa para altas nuevas).
CONCEPTO_PAGO_A_CUENTA = "Pago a cuenta"


def _conceptos_cobro_query(db: Session):
    return db.query(Concepto).filter(Concepto.desc_concepto.in_(CONCEPTOS_COBRO))


class ConceptoCobroOut(BaseModel):
    id_concepto: int
    desc_concepto: str


class CobroCreateIn(BaseModel):
    fcha_cobro: date
    conceptos_id_concepto: int
    importe: Decimal
    rendido: str = "N"
    detalle: str | None = None


class CobroOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cobros: int
    cuentas_id_cta: int
    fcha_cobro: date | None = None
    concepto: str | None = None
    detalle: str | None = None
    importe: Decimal | None = None
    rendido: str | None = None
    anulado: str | None = None
    anulado_por_nombre: str | None = None
    anulado_ts: datetime | None = None


@router.get("/catalogos/conceptos-cobro", response_model=list[ConceptoCobroOut])
def listar_conceptos_cobro(db: Session = Depends(get_db), _user: dict = Depends(get_current_user)):
    """Los dos únicos conceptos habilitados para cargar un cobro."""
    filas = _conceptos_cobro_query(db).order_by(Concepto.desc_concepto).all()
    if not filas:
        raise HTTPException(
            status_code=500,
            detail="Los conceptos de cobro (CAPITAL/HONORARIOS) no están cargados. "
                   "Ejecutá el seed 05-conceptos-cobros.sql en la base de datos.",
        )
    return filas


def _cobro_a_out(cobro: Cobro, concepto_desc: str | None, anulado_por_nombre: str | None) -> CobroOut:
    return CobroOut(
        id_cobros=cobro.id_cobros,
        cuentas_id_cta=cobro.cuentas_id_cta,
        fcha_cobro=cobro.fcha_cobro,
        concepto=concepto_desc or CONCEPTO_PAGO_A_CUENTA,
        detalle=cobro.desc_cobro,
        importe=cobro.importe,
        rendido=cobro.rendido,
        anulado=cobro.anulado,
        anulado_por_nombre=anulado_por_nombre,
        anulado_ts=cobro.anulado_ts,
    )


@router.post("/cuentas/{id_cta}/cobros", response_model=CobroOut, status_code=status.HTTP_201_CREATED)
def crear_cobro(
    id_cta: int,
    payload: CobroCreateIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    if not db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first():
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    concepto = (
        _conceptos_cobro_query(db)
        .filter(Concepto.id_concepto == payload.conceptos_id_concepto)
        .first()
    )
    if not concepto:
        raise HTTPException(status_code=400, detail="Concepto inválido: debe ser CAPITAL o HONORARIOS")

    if payload.rendido not in ("S", "N"):
        raise HTTPException(status_code=400, detail="rendido debe ser 'S' o 'N'")

    if payload.importe <= 0:
        raise HTTPException(status_code=400, detail="El importe debe ser mayor a 0")

    # cobros.movimientos_id_mov es NOT NULL: cada cobro genera su propio
    # movimiento de caja (ingreso).
    movimiento = Movimiento(
        importe_ingreso_mov=payload.importe,
        fecha_mov=payload.fcha_cobro,
        desc_mov=f"Cobro cuenta {id_cta} - {concepto.desc_concepto}",
        anulado_mov="N",
    )
    db.add(movimiento)
    db.flush()

    nuevo = Cobro(
        movimientos_id_mov=movimiento.id_mov,
        conceptos_id_concepto=concepto.id_concepto,
        cuentas_id_cta=id_cta,
        fcha_cobro=payload.fcha_cobro,
        desc_cobro=(payload.detalle or "").strip() or None,
        importe=payload.importe,
        rendido=payload.rendido,
        anulado="N",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return _cobro_a_out(nuevo, concepto.desc_concepto, None)


@router.patch("/cobros/{id_cobros}/anular")
def anular_cobro(
    id_cobros: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Anula un cobro (soft-delete, con trazabilidad de quién y cuándo). Nunca se borra
    de la base: mantiene el historial para auditoría."""
    cobro = db.query(Cobro).filter(Cobro.id_cobros == id_cobros).first()
    if not cobro:
        raise HTTPException(status_code=404, detail="Cobro no encontrado")
    if cobro.anulado == "S":
        raise HTTPException(status_code=400, detail="El cobro ya está anulado")

    cobro.anulado = "S"
    cobro.anulado_por = _user["id_usuario"]
    cobro.anulado_ts = datetime.now(timezone.utc)

    movimiento = db.query(Movimiento).filter(Movimiento.id_mov == cobro.movimientos_id_mov).first()
    if movimiento:
        movimiento.anulado_mov = "S"

    db.commit()
    return {"message": "Cobro anulado"}
