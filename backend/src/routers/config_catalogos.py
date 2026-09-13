"""
Router de administración de catálogos: Estados, SubEstados, Acciones, Resultados, Conceptos,
Clientes y Subclientes. Todos los endpoints están gateados con `get_current_admin`.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_admin
from src.models.cuentas import Cliente, Subcliente
from src.models.catalogos import Estado, SubEstado, Accion, Resultado, Concepto

router = APIRouter(prefix="/config", tags=["Configuración"])


# ============================================================================
# CLIENTE
# ============================================================================

class ClienteCreateIn(BaseModel):
    cuenta_cliente: int
    desc_cliente: str


class ClienteUpdateIn(BaseModel):
    desc_cliente: Optional[str] = None


class ClienteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cliente: int
    cuenta_cliente: int
    desc_cliente: str
    activo: str


@router.get("/clientes", response_model=list[ClienteOut])
def listar_clientes(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todos los clientes ordenados por PK."""
    clientes = db.query(Cliente).order_by(Cliente.id_cliente, Cliente.cuenta_cliente).all()
    return clientes


@router.get("/clientes/{id_cliente}/{cuenta_cliente}", response_model=ClienteOut)
def obtener_cliente(
    id_cliente: int,
    cuenta_cliente: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de un cliente por id_cliente y cuenta_cliente."""
    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == id_cliente,
        Cliente.cuenta_cliente == cuenta_cliente,
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/clientes", response_model=ClienteOut, status_code=201)
def crear_cliente(
    payload: ClienteCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear un nuevo cliente. id_cliente es autoincremental, lo asigna la DB."""
    nuevo = Cliente(
        cuenta_cliente=payload.cuenta_cliente,
        desc_cliente=payload.desc_cliente,
        activo="S",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/clientes/{id_cliente}/{cuenta_cliente}", response_model=ClienteOut)
def actualizar_cliente(
    id_cliente: int,
    cuenta_cliente: int,
    payload: ClienteUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar un cliente existente."""
    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == id_cliente,
        Cliente.cuenta_cliente == cuenta_cliente,
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    if payload.desc_cliente is not None:
        cliente.desc_cliente = payload.desc_cliente

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/clientes/{id_cliente}/{cuenta_cliente}")
def eliminar_cliente(
    id_cliente: int,
    cuenta_cliente: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja un cliente (soft-delete)."""
    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == id_cliente,
        Cliente.cuenta_cliente == cuenta_cliente,
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    cliente.activo = "N"
    db.commit()
    return {"message": f"Cliente {id_cliente}/{cuenta_cliente} dado de baja"}


# ============================================================================
# SUBCLIENTE
# ============================================================================

class SubclienteCreateIn(BaseModel):
    clientes_id_cliente: int
    clientes_cuenta_cliente: int
    nombre_subcli: str
    decuento_subcli: Optional[float] = None
    porccomi_subcli: Optional[float] = None
    porcquita_subcli: Optional[float] = None
    porcact_subcli: Optional[float] = None
    plazogestion_subcli: Optional[int] = None


class SubclienteUpdateIn(BaseModel):
    clientes_id_cliente: Optional[int] = None
    clientes_cuenta_cliente: Optional[int] = None
    nombre_subcli: Optional[str] = None
    decuento_subcli: Optional[float] = None
    porccomi_subcli: Optional[float] = None
    porcquita_subcli: Optional[float] = None
    porcact_subcli: Optional[float] = None
    plazogestion_subcli: Optional[int] = None


class SubclienteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_subcli: int
    clientes_id_cliente: int
    clientes_cuenta_cliente: int
    cliente_nombre: Optional[str] = None
    nombre_subcli: str
    decuento_subcli: Optional[float] = None
    porccomi_subcli: Optional[float] = None
    porcquita_subcli: Optional[float] = None
    porcact_subcli: Optional[float] = None
    plazogestion_subcli: Optional[int] = None
    activo_subcli: str


@router.get("/subclientes", response_model=list[SubclienteOut])
def listar_subclientes(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todos los subclientes ordenados por PK."""
    subclientes = (
        db.query(Subcliente, Cliente.desc_cliente)
        .join(Cliente, (Subcliente.clientes_id_cliente == Cliente.id_cliente) &
                      (Subcliente.clientes_cuenta_cliente == Cliente.cuenta_cliente))
        .order_by(Subcliente.id_subcli)
        .all()
    )

    results = []
    for sub, desc in subclientes:
        item = Subcliente(
            id_subcli=sub.id_subcli,
            clientes_id_cliente=sub.clientes_id_cliente,
            clientes_cuenta_cliente=sub.clientes_cuenta_cliente,
            nombre_subcli=sub.nombre_subcli,
            decuento_subcli=sub.decuento_subcli,
            porccomi_subcli=sub.porccomi_subcli,
            porcquita_subcli=sub.porcquita_subcli,
            porcact_subcli=sub.porcact_subcli,
            plazogestion_subcli=sub.plazogestion_subcli,
            activo_subcli=sub.activo_subcli,
        )
        # Inject the joined field
        setattr(item, "cliente_nombre", desc)
        results.append(item)

    return results


@router.get("/subclientes/{id_subcli}", response_model=SubclienteOut)
def obtener_subcliente(
    id_subcli: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de un subcliente."""
    subcliente = db.query(Subcliente).filter(Subcliente.id_subcli == id_subcli).first()
    if not subcliente:
        raise HTTPException(status_code=404, detail="Subcliente no encontrado")
    return subcliente


@router.post("/subclientes", response_model=SubclienteOut, status_code=201)
def crear_subcliente(
    payload: SubclienteCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear un nuevo subcliente."""
    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == payload.clientes_id_cliente,
        Cliente.cuenta_cliente == payload.clientes_cuenta_cliente,
    ).first()
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente inexistente")

    nuevo = Subcliente(
        clientes_id_cliente=payload.clientes_id_cliente,
        clientes_cuenta_cliente=payload.clientes_cuenta_cliente,
        nombre_subcli=payload.nombre_subcli,
        decuento_subcli=payload.decuento_subcli,
        porccomi_subcli=payload.porccomi_subcli,
        porcquita_subcli=payload.porcquita_subcli,
        porcact_subcli=payload.porcact_subcli,
        plazogestion_subcli=payload.plazogestion_subcli,
        activo_subcli="S",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/subclientes/{id_subcli}", response_model=SubclienteOut)
def actualizar_subcliente(
    id_subcli: int,
    payload: SubclienteUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar un subcliente existente."""
    subcliente = db.query(Subcliente).filter(Subcliente.id_subcli == id_subcli).first()
    if not subcliente:
        raise HTTPException(status_code=404, detail="Subcliente no encontrado")

    if payload.clientes_id_cliente is not None or payload.clientes_cuenta_cliente is not None:
        nuevo_id = payload.clientes_id_cliente if payload.clientes_id_cliente is not None else subcliente.clientes_id_cliente
        nueva_cuenta = payload.clientes_cuenta_cliente if payload.clientes_cuenta_cliente is not None else subcliente.clientes_cuenta_cliente
        cliente = db.query(Cliente).filter(
            Cliente.id_cliente == nuevo_id,
            Cliente.cuenta_cliente == nueva_cuenta,
        ).first()
        if not cliente:
            raise HTTPException(status_code=400, detail="Cliente inexistente")
        subcliente.clientes_id_cliente = nuevo_id
        subcliente.clientes_cuenta_cliente = nueva_cuenta
    if payload.nombre_subcli is not None:
        subcliente.nombre_subcli = payload.nombre_subcli
    if payload.decuento_subcli is not None:
        subcliente.decuento_subcli = payload.decuento_subcli
    if payload.porccomi_subcli is not None:
        subcliente.porccomi_subcli = payload.porccomi_subcli
    if payload.porcquita_subcli is not None:
        subcliente.porcquita_subcli = payload.porcquita_subcli
    if payload.porcact_subcli is not None:
        subcliente.porcact_subcli = payload.porcact_subcli
    if payload.plazogestion_subcli is not None:
        subcliente.plazogestion_subcli = payload.plazogestion_subcli

    db.commit()
    db.refresh(subcliente)
    return subcliente


@router.delete("/subclientes/{id_subcli}")
def eliminar_subcliente(
    id_subcli: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja un subcliente (soft-delete)."""
    subcliente = db.query(Subcliente).filter(Subcliente.id_subcli == id_subcli).first()
    if not subcliente:
        raise HTTPException(status_code=404, detail="Subcliente no encontrado")

    subcliente.activo_subcli = "N"
    db.commit()
    return {"message": f"Subcliente {id_subcli} dado de baja"}


# ============================================================================
# ESTADO
# ============================================================================

class EstadoCreateIn(BaseModel):
    desc_estado: str
    tipo_estado: str


class EstadoUpdateIn(BaseModel):
    desc_estado: Optional[str] = None
    tipo_estado: Optional[str] = None


class EstadoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_estado: int
    desc_estado: str
    tipo_estado: str
    activo: str


@router.get("/estados", response_model=list[EstadoOut])
def listar_estados(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todos los estados ordenados por PK."""
    estados = db.query(Estado).order_by(Estado.id_estado).all()
    return estados


@router.get("/estados/{id_estado}", response_model=EstadoOut)
def obtener_estado(
    id_estado: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de un estado."""
    estado = db.query(Estado).filter(Estado.id_estado == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado


@router.post("/estados", response_model=EstadoOut, status_code=201)
def crear_estado(
    payload: EstadoCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear un nuevo estado."""
    nuevo = Estado(
        desc_estado=payload.desc_estado,
        tipo_estado=payload.tipo_estado,
        activo="S",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/estados/{id_estado}", response_model=EstadoOut)
def actualizar_estado(
    id_estado: int,
    payload: EstadoUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar un estado existente."""
    estado = db.query(Estado).filter(Estado.id_estado == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    if payload.desc_estado is not None:
        estado.desc_estado = payload.desc_estado
    if payload.tipo_estado is not None:
        estado.tipo_estado = payload.tipo_estado

    db.commit()
    db.refresh(estado)
    return estado


@router.delete("/estados/{id_estado}")
def eliminar_estado(
    id_estado: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja un estado (soft-delete)."""
    estado = db.query(Estado).filter(Estado.id_estado == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    estado.activo = "N"
    db.commit()
    return {"message": f"Estado {id_estado} dado de baja"}


# ============================================================================
# SUB-ESTADO
# ============================================================================

class SubEstadoCreateIn(BaseModel):
    estados_id_estado: int
    desc_sub_est: str


class SubEstadoUpdateIn(BaseModel):
    desc_sub_est: Optional[str] = None
    estados_id_estado: Optional[int] = None


class SubEstadoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_sub_est: int
    estados_id_estado: int
    desc_sub_est: str
    activo: str


@router.get("/sub-estados", response_model=list[SubEstadoOut])
def listar_sub_estados(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todos los sub-estados ordenados por PK."""
    sub_estados = db.query(SubEstado).order_by(SubEstado.id_sub_est).all()
    return sub_estados


@router.get("/sub-estados/{id_sub_est}", response_model=SubEstadoOut)
def obtener_sub_estado(
    id_sub_est: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de un sub-estado."""
    sub_estado = db.query(SubEstado).filter(SubEstado.id_sub_est == id_sub_est).first()
    if not sub_estado:
        raise HTTPException(status_code=404, detail="Sub-estado no encontrado")
    return sub_estado


@router.post("/sub-estados", response_model=SubEstadoOut, status_code=201)
def crear_sub_estado(
    payload: SubEstadoCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear un nuevo sub-estado."""
    # Validar que el estado padre existe
    estado_padre = db.query(Estado).filter(Estado.id_estado == payload.estados_id_estado).first()
    if not estado_padre:
        raise HTTPException(status_code=404, detail="Estado padre no encontrado")

    nuevo = SubEstado(
        estados_id_estado=payload.estados_id_estado,
        desc_sub_est=payload.desc_sub_est,
        activo="S",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/sub-estados/{id_sub_est}", response_model=SubEstadoOut)
def actualizar_sub_estado(
    id_sub_est: int,
    payload: SubEstadoUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar un sub-estado existente."""
    sub_estado = db.query(SubEstado).filter(SubEstado.id_sub_est == id_sub_est).first()
    if not sub_estado:
        raise HTTPException(status_code=404, detail="Sub-estado no encontrado")

    if payload.desc_sub_est is not None:
        sub_estado.desc_sub_est = payload.desc_sub_est
    if payload.estados_id_estado is not None:
        estado_padre = db.query(Estado).filter(Estado.id_estado == payload.estados_id_estado).first()
        if not estado_padre:
            raise HTTPException(status_code=404, detail="Estado padre no encontrado")
        sub_estado.estados_id_estado = payload.estados_id_estado

    db.commit()
    db.refresh(sub_estado)
    return sub_estado


@router.delete("/sub-estados/{id_sub_est}")
def eliminar_sub_estado(
    id_sub_est: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja un sub-estado (soft-delete)."""
    sub_estado = db.query(SubEstado).filter(SubEstado.id_sub_est == id_sub_est).first()
    if not sub_estado:
        raise HTTPException(status_code=404, detail="Sub-estado no encontrado")

    sub_estado.activo = "N"
    db.commit()
    return {"message": f"Sub-estado {id_sub_est} dado de baja"}


# ============================================================================
# ACCION
# ============================================================================

class AccionCreateIn(BaseModel):
    desc_accion: str


class AccionUpdateIn(BaseModel):
    desc_accion: Optional[str] = None


class AccionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_accion: int
    desc_accion: str
    activa: str


@router.get("/acciones", response_model=list[AccionOut])
def listar_acciones(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todas las acciones ordenadas por PK."""
    acciones = db.query(Accion).order_by(Accion.id_accion).all()
    return acciones


@router.get("/acciones/{id_accion}", response_model=AccionOut)
def obtener_accion(
    id_accion: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de una acción."""
    accion = db.query(Accion).filter(Accion.id_accion == id_accion).first()
    if not accion:
        raise HTTPException(status_code=404, detail="Acción no encontrada")
    return accion


@router.post("/acciones", response_model=AccionOut, status_code=201)
def crear_accion(
    payload: AccionCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear una nueva acción."""
    nueva = Accion(
        desc_accion=payload.desc_accion,
        activa="S",
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.patch("/acciones/{id_accion}", response_model=AccionOut)
def actualizar_accion(
    id_accion: int,
    payload: AccionUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar una acción existente."""
    accion = db.query(Accion).filter(Accion.id_accion == id_accion).first()
    if not accion:
        raise HTTPException(status_code=404, detail="Acción no encontrada")

    if payload.desc_accion is not None:
        accion.desc_accion = payload.desc_accion

    db.commit()
    db.refresh(accion)
    return accion


@router.delete("/acciones/{id_accion}")
def eliminar_accion(
    id_accion: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja una acción (soft-delete)."""
    accion = db.query(Accion).filter(Accion.id_accion == id_accion).first()
    if not accion:
        raise HTTPException(status_code=404, detail="Acción no encontrada")

    accion.activa = "N"
    db.commit()
    return {"message": f"Acción {id_accion} dado de baja"}


# ============================================================================
# RESULTADO
# ============================================================================

class ResultadoCreateIn(BaseModel):
    desc_resultado: str
    positivo: str


class ResultadoUpdateIn(BaseModel):
    desc_resultado: Optional[str] = None
    positivo: Optional[str] = None


class ResultadoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_resultado: int
    desc_resultado: str
    positivo: str
    activo: str


@router.get("/resultados", response_model=list[ResultadoOut])
def listar_resultados(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todos los resultados ordenados por PK."""
    resultados = db.query(Resultado).order_by(Resultado.id_resultado).all()
    return resultados


@router.get("/resultados/{id_resultado}", response_model=ResultadoOut)
def obtener_resultado(
    id_resultado: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de un resultado."""
    resultado = db.query(Resultado).filter(Resultado.id_resultado == id_resultado).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado


@router.post("/resultados", response_model=ResultadoOut, status_code=201)
def crear_resultado(
    payload: ResultadoCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear un nuevo resultado."""
    nuevo = Resultado(
        desc_resultado=payload.desc_resultado,
        positivo=payload.positivo,
        activo="S",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/resultados/{id_resultado}", response_model=ResultadoOut)
def actualizar_resultado(
    id_resultado: int,
    payload: ResultadoUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar un resultado existente."""
    resultado = db.query(Resultado).filter(Resultado.id_resultado == id_resultado).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")

    if payload.desc_resultado is not None:
        resultado.desc_resultado = payload.desc_resultado
    if payload.positivo is not None:
        resultado.positivo = payload.positivo

    db.commit()
    db.refresh(resultado)
    return resultado


@router.delete("/resultados/{id_resultado}")
def eliminar_resultado(
    id_resultado: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja un resultado (soft-delete)."""
    resultado = db.query(Resultado).filter(Resultado.id_resultado == id_resultado).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")

    resultado.activo = "N"
    db.commit()
    return {"message": f"Resultado {id_resultado} dado de baja"}


# ============================================================================
# CONCEPTO
# ============================================================================

class ConceptoCreateIn(BaseModel):
    rubros_id_rubro: int
    desc_concepto: str


class ConceptoUpdateIn(BaseModel):
    desc_concepto: Optional[str] = None
    rubros_id_rubro: Optional[int] = None


class ConceptoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_concepto: int
    rubros_id_rubro: int
    desc_concepto: str
    activo: str


@router.get("/conceptos", response_model=list[ConceptoOut])
def listar_conceptos(
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Listar todos los conceptos ordenados por PK."""
    conceptos = db.query(Concepto).order_by(Concepto.id_concepto).all()
    return conceptos


@router.get("/conceptos/{id_concepto}", response_model=ConceptoOut)
def obtener_concepto(
    id_concepto: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Obtener detalle de un concepto."""
    concepto = db.query(Concepto).filter(Concepto.id_concepto == id_concepto).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")
    return concepto


@router.post("/conceptos", response_model=ConceptoOut, status_code=201)
def crear_concepto(
    payload: ConceptoCreateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Crear un nuevo concepto."""
    nuevo = Concepto(
        rubros_id_rubro=payload.rubros_id_rubro,
        desc_concepto=payload.desc_concepto,
        activo="S",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.patch("/conceptos/{id_concepto}", response_model=ConceptoOut)
def actualizar_concepto(
    id_concepto: int,
    payload: ConceptoUpdateIn,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Editar un concepto existente."""
    concepto = db.query(Concepto).filter(Concepto.id_concepto == id_concepto).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")

    if payload.desc_concepto is not None:
        concepto.desc_concepto = payload.desc_concepto
    if payload.rubros_id_rubro is not None:
        concepto.rubros_id_rubro = payload.rubros_id_rubro

    db.commit()
    db.refresh(concepto)
    return concepto


@router.delete("/conceptos/{id_concepto}")
def eliminar_concepto(
    id_concepto: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(get_current_admin),
):
    """Dar de baja un concepto (soft-delete)."""
    concepto = db.query(Concepto).filter(Concepto.id_concepto == id_concepto).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")

    concepto.activo = "N"
    db.commit()
    return {"message": f"Concepto {id_concepto} dado de baja"}
