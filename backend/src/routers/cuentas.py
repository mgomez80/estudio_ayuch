from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.auth_database import get_auth_db
from src.core.security import get_current_user
from src.models.cuentas import Cuenta, Entidad, Cliente, Subcliente
from src.models.catalogos import Estado, SubEstado
from src.models.contactos import Contacto
from src.models.financiero import Convenio, Cobro
from src.models.schemas import (
    CuentaOut,
    CuentaDetalleOut,
    ContactoOut,
    ConvenioOut,
    CobroOut,
)

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])


@router.get("/buscar", response_model=list[CuentaOut])
def buscar_cuentas(
    matricula: Optional[str] = Query(None, description="DNI/CUIT del deudor (matrícula)"),
    nombre: Optional[str] = Query(None, description="Nombre o razón social, búsqueda parcial"),
    estado_id: Optional[int] = Query(None, description="Filtrar por id de estado"),
    activa: Optional[str] = Query("S", description="S=activa, N=inactiva, omitir para todas"),
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """
    Búsqueda de cuentas por matrícula del deudor, nombre parcial, y/o estado.
    Al menos uno de matricula/nombre/estado_id debe especificarse para evitar
    traer toda la tabla por accidente.
    """
    if not matricula and not nombre and estado_id is None:
        raise HTTPException(
            status_code=400,
            detail="Especificá al menos un filtro: matricula, nombre o estado_id",
        )

    query = db.query(Cuenta)

    if matricula:
        # Prefijo: permite búsqueda en vivo con documento parcial desde el buscador
        query = query.filter(Cuenta.entidades_matricula_ent.like(f"{matricula}%"))

    if nombre:
        # Coincidencia por palabras: cada palabra debe aparecer en la razón social
        # (AND de LIKEs). "roberto garcia" matchea "Roberto Daniel García".
        query = query.join(Entidad, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
        for palabra in nombre.split():
            query = query.filter(Entidad.razon_social_ent.like(f"%{palabra}%"))

    if estado_id is not None:
        query = query.filter(Cuenta.estados_id_estado == estado_id)

    if activa:
        query = query.filter(Cuenta.activa_cta == activa)

    cuentas = query.order_by(Cuenta.id_cta.desc()).offset(offset).limit(limit).all()

    resultados = []
    for cuenta in cuentas:
        item = CuentaOut.model_validate(cuenta)
        item.razon_social_ent = cuenta.entidad.razon_social_ent if cuenta.entidad else None
        resultados.append(item)

    return resultados


class SubEstadoIn(BaseModel):
    id_sub_est: int


@router.patch("/{id_cta}/sub-estado")
def cambiar_sub_estado(
    id_cta: int,
    payload: SubEstadoIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    cuenta = db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail=f"Cuenta {id_cta} no encontrada")

    sub_estado = db.query(SubEstado).filter(SubEstado.id_sub_est == payload.id_sub_est).first()
    if not sub_estado:
        raise HTTPException(status_code=400, detail="Sub-estado inexistente")

    cuenta.sub_estados_id_sub_est = sub_estado.id_sub_est
    cuenta.estados_id_estado = sub_estado.estados_id_estado
    db.commit()
    return {"sub_estados_id_sub_est": sub_estado.id_sub_est, "estados_id_estado": sub_estado.estados_id_estado}


def _construir_detalle(db: Session, cuenta: Cuenta) -> CuentaDetalleOut:
    entidad = db.query(Entidad).filter(Entidad.matricula_ent == cuenta.entidades_matricula_ent).first()

    estado = db.query(Estado).filter(Estado.id_estado == cuenta.estados_id_estado).first()
    sub_estado = (
        db.query(SubEstado).filter(SubEstado.id_sub_est == cuenta.sub_estados_id_sub_est).first()
    )

    subcliente = (
        db.query(Subcliente).filter(Subcliente.id_subcli == cuenta.subclientes_id_subcli).first()
    )
    cliente = None
    if subcliente:
        cliente = (
            db.query(Cliente)
            .filter(
                Cliente.id_cliente == subcliente.clientes_id_cliente,
                Cliente.cuenta_cliente == subcliente.clientes_cuenta_cliente,
            )
            .first()
        )

    resultado = CuentaDetalleOut.model_validate(cuenta)
    resultado.razon_social_ent = entidad.razon_social_ent if entidad else None
    resultado.estado_desc = estado.desc_estado if estado else None
    resultado.sub_estado_desc = sub_estado.desc_sub_est if sub_estado else None
    resultado.cliente_desc = cliente.desc_cliente if cliente else None
    resultado.subcliente_nombre = subcliente.nombre_subcli if subcliente else None

    if entidad:
        resultado.entidad = entidad
        resultado.telefonos = entidad.telefonos
        resultado.direcciones = entidad.direcciones
        resultado.mails = entidad.mails

    return resultado


@router.get("/{id_cta}", response_model=CuentaDetalleOut)
def obtener_cuenta(
    id_cta: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Detalle completo de una cuenta: datos del deudor, cliente/subcliente, teléfonos, direcciones, mails."""
    cuenta = db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail=f"Cuenta {id_cta} no encontrada")
    return _construir_detalle(db, cuenta)


class CuentaUpdateIn(BaseModel):
    matricula: Optional[str] = Field(None, min_length=1, max_length=30)
    razon_social: Optional[str] = Field(None, min_length=1, max_length=200)
    deudaact_cta: Optional[Decimal] = Field(None, ge=0)
    deudatrans_cta: Optional[Decimal] = Field(None, ge=0)
    empleador_cta: Optional[str] = Field(None, max_length=200)
    observacion_cta: Optional[str] = Field(None, max_length=250)
    subclientes_id_subcli: Optional[int] = None
    cuenta_cliente: Optional[str] = Field(None, max_length=50)


@router.patch("/{id_cta}", response_model=CuentaDetalleOut)
def editar_cuenta(
    id_cta: int,
    payload: CuentaUpdateIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Edita los datos de una cuenta, incluida la matrícula del deudor. Cambiar la
    matrícula renombra la entidad y todo lo que cuelga de ella (otras cuentas del
    mismo deudor, teléfonos, direcciones, mails) para no dejar registros huérfanos."""
    cuenta = db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail=f"Cuenta {id_cta} no encontrada")

    if payload.subclientes_id_subcli is not None:
        subcli = db.query(Subcliente).filter(
            Subcliente.id_subcli == payload.subclientes_id_subcli,
            Subcliente.activo_subcli == "S",
        ).first()
        if not subcli:
            raise HTTPException(status_code=400, detail="Subcliente inexistente o inactivo")
        cuenta.subclientes_id_subcli = payload.subclientes_id_subcli

    if payload.matricula is not None:
        nueva = payload.matricula.strip()
        vieja = cuenta.entidades_matricula_ent
        if nueva != vieja:
            if db.query(Entidad).filter(Entidad.matricula_ent == nueva).first():
                raise HTTPException(status_code=400, detail=f"Ya existe una entidad con matrícula {nueva}")
            entidad = db.query(Entidad).filter(Entidad.matricula_ent == vieja).first()
            if not entidad:
                raise HTTPException(status_code=404, detail=f"Entidad {vieja} no encontrada")
            # Todo lo que referencia la matrícula vieja por columna (no hay FK real
            # en este esquema) se renombra primero; la entidad (su PK) se cambia al final.
            from src.models.contactos import Telefono, Direccion, Mail
            db.query(Cuenta).filter(Cuenta.entidades_matricula_ent == vieja).update(
                {"entidades_matricula_ent": nueva}, synchronize_session=False)
            db.query(Telefono).filter(Telefono.entidades_matricula_ent == vieja).update(
                {"entidades_matricula_ent": nueva}, synchronize_session=False)
            db.query(Direccion).filter(Direccion.entidades_matricula_ent == vieja).update(
                {"entidades_matricula_ent": nueva}, synchronize_session=False)
            db.query(Mail).filter(Mail.entidades_matricula_ent == vieja).update(
                {"entidades_matricula_ent": nueva}, synchronize_session=False)
            entidad.matricula_ent = nueva
            # El bulk .update() de arriba no sincroniza el objeto ya cargado en
            # memoria: sin esto, el resto del request seguiría viendo la matrícula
            # vieja (rompiendo, por ejemplo, la edición de razón social debajo).
            cuenta.entidades_matricula_ent = nueva
            db.flush()

    if payload.razon_social is not None:
        entidad = db.query(Entidad).filter(Entidad.matricula_ent == cuenta.entidades_matricula_ent).first()
        if entidad:
            entidad.razon_social_ent = payload.razon_social.strip().upper()

    if payload.deudaact_cta is not None:
        cuenta.deudaact_cta = payload.deudaact_cta
    if payload.deudatrans_cta is not None:
        cuenta.deudatrans_cta = payload.deudatrans_cta
    if payload.empleador_cta is not None:
        cuenta.empleador_cta = payload.empleador_cta
    if payload.observacion_cta is not None:
        cuenta.observacion_cta = payload.observacion_cta
    if payload.cuenta_cliente is not None:
        cuenta.cuenta_cliente = payload.cuenta_cliente

    db.commit()
    db.refresh(cuenta)
    return _construir_detalle(db, cuenta)


@router.get("/{id_cta}/contactos", response_model=list[ContactoOut])
def historial_contactos(
    id_cta: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    db_auth: Session = Depends(get_auth_db),
    _user: dict = Depends(get_current_user),
):
    """Historial de gestión (llamadas, whatsapp, etc.) de una cuenta, más reciente primero.
    Incluye los dados de baja (la baja es lógica, no se borran del historial)."""
    from src.models.catalogos import Accion, Resultado
    from src.models.usuario import Usuario

    contactos = (
        db.query(Contacto)
        .filter(Contacto.cuentas_id_cta == id_cta)
        .order_by(Contacto.fecha_contacto.desc(), Contacto.id_contacto.desc())
        .limit(limit)
        .all()
    )

    resultado = []
    for c in contactos:
        item = ContactoOut.model_validate(c)
        accion = db.query(Accion).filter(Accion.id_accion == c.acciones_id_accion).first()
        res = db.query(Resultado).filter(Resultado.id_resultado == c.resultados_id_resultado).first()
        usuario = db_auth.query(Usuario).filter(Usuario.id_usuario == c.usuarios_id_usuario).first()
        item.desc_accion = accion.desc_accion if accion else None
        item.desc_resultado = res.desc_resultado if res else None
        item.usuario_nombre = usuario.loguin_usuario if usuario else None
        item.nota_contacto = c.nota_contacto.decode() if c.nota_contacto else None
        resultado.append(item)

    return resultado


@router.get("/{id_cta}/convenios", response_model=list[ConvenioOut])
def convenios_de_cuenta(
    id_cta: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Planes de pago (convenios) asociados a una cuenta."""
    return db.query(Convenio).filter(Convenio.cuentas_id_cta == id_cta).all()


@router.get("/{id_cta}/cobros", response_model=list[CobroOut])
def cobros_de_cuenta(
    id_cta: int,
    db: Session = Depends(get_db),
    auth_db: Session = Depends(get_auth_db),
    _user: dict = Depends(get_current_user),
):
    """Pagos recibidos para una cuenta, más reciente primero. Incluye anulados (con trazabilidad)."""
    from src.models.usuario import Usuario
    from src.models.catalogos import Concepto
    from src.routers.cobros_abm import CONCEPTO_PAGO_A_CUENTA

    filas = (
        db.query(Cobro, Concepto.desc_concepto)
        .outerjoin(Concepto, Cobro.conceptos_id_concepto == Concepto.id_concepto)
        .filter(Cobro.cuentas_id_cta == id_cta)
        .order_by(Cobro.fcha_cobro.desc())
        .all()
    )
    out = []
    for c, concepto_desc in filas:
        item = CobroOut.model_validate(c)
        item.concepto = concepto_desc or CONCEPTO_PAGO_A_CUENTA
        if c.anulado == "S" and c.anulado_por:
            item.anulado_por_nombre = (
                auth_db.query(Usuario.loguin_usuario)
                .filter(Usuario.id_usuario == c.anulado_por)
                .scalar()
            )
        out.append(item)
    return out


# ---------------------------------------------------------------------------
# Alta simple: crea la entidad (si no existe) y la cuenta en un solo paso.
# Usado por el botón "Carga simple" del frontend.
# ---------------------------------------------------------------------------
from datetime import date as _date


class AltaSimpleIn(BaseModel):
    matricula: str = Field(min_length=6, max_length=30, pattern=r"^\d+$")
    razon_social: str = Field(min_length=3, max_length=200)
    id_subcli: int
    deudaact: Decimal = Field(ge=0)
    cuenta_cliente: Optional[str] = Field(None, max_length=50)
    observacion: Optional[str] = Field(None, max_length=250)


@router.post("/alta-simple", response_model=CuentaOut, status_code=201)
def alta_simple(
    payload: AltaSimpleIn,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Crea entidad + cuenta. Si la entidad ya existe, solo agrega la cuenta."""
    subcli = db.query(Subcliente).filter(
        Subcliente.id_subcli == payload.id_subcli,
        Subcliente.activo_subcli == "S",
    ).first()
    if not subcli:
        raise HTTPException(status_code=400, detail="Subcliente inexistente o inactivo")

    entidad = db.query(Entidad).filter(Entidad.matricula_ent == payload.matricula).first()
    if entidad is None:
        entidad = Entidad(
            matricula_ent=payload.matricula,
            razon_social_ent=payload.razon_social.strip().upper(),
            activo_ent="S",
        )
        db.add(entidad)

    sub_estado_inicial = db.query(SubEstado).filter(
        SubEstado.desc_sub_est.ilike("en gestion")
    ).first()
    if not sub_estado_inicial:
        raise HTTPException(
            status_code=500,
            detail="Sub_estado 'EN GESTION' no está cargado en la tabla sub_estados",
        )

    cuenta = Cuenta(
        entidades_matricula_ent=payload.matricula,
        subclientes_id_subcli=payload.id_subcli,
        cuenta_cliente=payload.cuenta_cliente,
        deudaact_cta=payload.deudaact,
        fechaingreso_cta=_date.today(),
        activa_cta="S",
        judicial="N",
        observacion_cta=payload.observacion,
        estados_id_estado=sub_estado_inicial.estados_id_estado,
        sub_estados_id_sub_est=sub_estado_inicial.id_sub_est,
    )
    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)

    return CuentaOut(
        id_cta=cuenta.id_cta,
        entidades_matricula_ent=cuenta.entidades_matricula_ent,
        estados_id_estado=cuenta.estados_id_estado,
        sub_estados_id_sub_est=cuenta.sub_estados_id_sub_est,
        cuenta_cliente=cuenta.cuenta_cliente,
        deudatrans_cta=cuenta.deudatrans_cta,
        deudaact_cta=cuenta.deudaact_cta,
        fechaingreso_cta=cuenta.fechaingreso_cta,
        empleador_cta=cuenta.empleador_cta,
        activa_cta=cuenta.activa_cta,
        judicial=cuenta.judicial,
        observacion_cta=cuenta.observacion_cta,
        razon_social_ent=entidad.razon_social_ent,
    )
