"""
Chat-Cobranza: catálogo de tools + system prompt del gestor IA (Hermes).

Funciones de lectura (consultan DB), informes (generan HTML), y acciones
(requieren confirmación). Handlers reusan modelos y helpers existentes.
"""

from datetime import date, datetime, timedelta
import json
from sqlalchemy import func, cast, Numeric, or_
from sqlalchemy.orm import Session

from src.models.cuentas import Cuenta, Entidad
from src.models.contactos import Contacto, Agenda, Telefono
from src.models.catalogos import Accion, Resultado
from src.models.financiero import Cobro, Convenio, Vencimiento
from src.models.judicial import Demanda

# La deuda se guarda como VARCHAR; casteamos para agregaciones
DEUDA_NUM = cast(Cuenta.deudaact_cta, Numeric(20, 2))

SYSTEM_PROMPT = """Sos un gestor senior de recupero de deuda extrajudicial en Acuerdo Cobranzas.

Tu rol:
- Asesorar sobre el estado de cuentas deudoras y cartera.
- Proponer acciones de recupero (WhatsApp, agenda, contactos).
- Generar informes descargables (PDF, planillas).
- Hablar en español rioplatense profesional.

Reglas:
1. **Datos siempre de las tools**: Nunca inventés cifras. Consultá buscar_cuentas, dossier_cuenta, resumen_cartera, etc.
2. **Referencias claras**: Al hablar de cuentas, citá el id_cta y la matrícula del deudor.
3. **Acciones con confirmación**: Cuando propongas enviar WhatsApp, crear agenda o registrar contacto, explicá qué vas a hacer y espera que el usuario confirme.
4. **Horario legal**: Respetá horario permitido de contacto (típico 08:00–20:00) al proponer acciones.
5. **Montos flotantes, fechas isoformat**: Los datos que devuelven las tools usan esos formatos.

Cómo generar informes (versátil y rápido):
- Si el pedido es conversacional ("cómo está la cartera", "quiénes deben más") alcanza con resumen_cartera/top_deudores/gestion_periodo/cobros_periodo — respondé directo en el chat, no generes un informe descargable.
- Si el pedido es explícito de informe/reporte/exportable/PDF/Excel/planilla, o el usuario lo pide después de ver un resumen, llamá generar_informe DIRECTO con parámetros razonables (ej. dias=90 si no especifica rango). No repitas una consulta exploratoria si ya tenés contexto suficiente del pedido — cada ida y vuelta de más suma latencia.
- Si el pedido necesita combinar varias fuentes (ej. cartera + gestión + cobros para una visión 360), pedí todas las tools que necesites en el mismo turno en vez de una por una.
- Al responder en el chat (no en el informe), usá formato profesional: resumen ejecutivo corto arriba, bullets o tabla para el detalle, montos con separador de miles ($ 1.234.567), sin relleno ni repetir el pedido del usuario.
- Después de generar un informe, ofrecé el PDF/Excel en una frase corta y preguntá si necesita algo más — sin explicar de nuevo lo que ya generaste.

No repreguntes, decidí como experto:
- Ante ambigüedad de rango/parámetro (fechas, cantidad, filtro), usá el default más razonable (últimos 90 días, top 10, cartera activa) y ACLARÁ el supuesto en una frase corta dentro de la misma respuesta — nunca cortes el flujo con una pregunta antes de consultar datos.
- Repreguntá SOLO si falta un dato imposible de inferir y bloqueante para ejecutar la tool correcta (ej. matrícula/id_cta ausente en un pedido puntual de cuenta, o falta destinatario/teléfono para una acción de WhatsApp). Para acciones (enviar_whatsapp, crear_agenda, registrar_contacto) la confirmación explícita del usuario ya cumple ese rol — no agregues una pregunta previa redundante.
- Si el usuario da información parcial pero suficiente para una interpretación razonable, actuá con esa interpretación y dejá la corrección para después si hace falta. Preferí una respuesta útil con supuesto explícito antes que una repregunta.

Objetivo: recuperar deuda extrajudicial de forma profesional y auditable.
"""

ACCIONES = {"enviar_whatsapp", "crear_agenda", "registrar_contacto"}


def es_accion(nombre: str) -> bool:
    """Retorna True si el nombre es una acción que requiere confirmación."""
    return nombre in ACCIONES


def _buscar_cuentas_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Busca cuentas por término (q). Retorna lista limitada a 20."""
    q = argumentos.get("q", "").strip()
    limite = argumentos.get("limite", 10)
    limite = min(limite, 20)

    if not q:
        return {"error": "Parámetro 'q' requerido"}

    # Buscar por matrícula exacta o nombre parcial
    query = db.query(Cuenta).filter(Cuenta.activa_cta == "S")

    # Si es numérico, buscar por id_cta o matrícula
    if q.isdigit():
        query = query.filter(
            or_(
                Cuenta.id_cta == int(q),
                Cuenta.entidades_matricula_ent == q
            )
        )
    else:
        # Búsqueda por nombre (join con Entidad)
        query = query.join(Entidad, Cuenta.entidades_matricula_ent == Entidad.matricula_ent)
        for palabra in q.split():
            query = query.filter(Entidad.razon_social_ent.like(f"%{palabra}%"))

    cuentas = query.order_by(Cuenta.deudaact_cta.desc()).limit(limite).all()

    resultados = []
    for c in cuentas:
        resultados.append({
            "id_cta": c.id_cta,
            "matricula": c.entidades_matricula_ent,
            "nombre": c.entidad.razon_social_ent if c.entidad else "—",
            "deuda": float(c.deudaact_cta or 0),
            "estado_id": c.estados_id_estado,
        })

    return {"cuentas": resultados}


def _dossier_cuenta_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Dossier completo de una cuenta: datos, deuda, teléfonos, señales, últimos contactos, convenios, cobros."""
    id_cta = argumentos.get("id_cta")
    if not id_cta:
        return {"error": "Parámetro 'id_cta' requerido"}

    cuenta = db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first()
    if not cuenta:
        return {"error": f"Cuenta {id_cta} no encontrada"}

    entidad = db.query(Entidad).filter(Entidad.matricula_ent == cuenta.entidades_matricula_ent).first()

    # Teléfonos
    telefonos = db.query(Telefono).filter(
        Telefono.entidades_matricula_ent == cuenta.entidades_matricula_ent,
        Telefono.activo_tel == "S"
    ).all()
    tels = [f"{t.codigo_area_tel}-{t.numero_tel}" for t in telefonos]

    # Señales: reusar _señales_batch (mandato spec). Import lazy: el router
    # arrastra settings de seguridad que no deben cargarse al importar este módulo.
    from src.routers.asistente import _señales_batch
    señales = _señales_batch(db, [id_cta]).get(id_cta, {
        "antiguedad_dias": 0,
        "judicial_activa": False,
        "gestiones_sin_resultado": 0,
        "promesa_incumplida": False,
        "convenio_caido": False,
    })

    # Últimos contactos (últimos 3): lookup batch de acciones/resultados
    contactos = db.query(Contacto).filter(
        Contacto.cuentas_id_cta == id_cta,
        Contacto.activo == "S"
    ).order_by(Contacto.fecha_contacto.desc()).limit(3).all()

    # Cargar catálogos en batch
    accion_ids = [c.acciones_id_accion for c in contactos if c.acciones_id_accion]
    resultado_ids = [c.resultados_id_resultado for c in contactos if c.resultados_id_resultado]

    acciones_map = {a.id_accion: a.desc_accion for a in db.query(Accion).filter(Accion.id_accion.in_(accion_ids)).all()} if accion_ids else {}
    resultados_map = {r.id_resultado: r.desc_resultado for r in db.query(Resultado).filter(Resultado.id_resultado.in_(resultado_ids)).all()} if resultado_ids else {}

    ultimos_contactos = []
    for c in contactos:
        ultimos_contactos.append({
            "fecha": c.fecha_contacto.isoformat() if c.fecha_contacto else None,
            "accion": acciones_map.get(c.acciones_id_accion, "—"),
            "resultado": resultados_map.get(c.resultados_id_resultado, "—"),
        })

    # Convenios activos con próximo vencimiento
    convenios = db.query(Convenio).filter(
        Convenio.cuentas_id_cta == id_cta,
        Convenio.cancelado != "S"
    ).all()

    convenio_ids = [conv.id_convenios for conv in convenios]
    vencimientos_map = {}
    if convenio_ids:
        vtos = db.query(Vencimiento).filter(
            Vencimiento.id_convenio.in_(convenio_ids),
            Vencimiento.pagado == "N"
        ).order_by(Vencimiento.fecha).all()
        for v in vtos:
            if v.id_convenio not in vencimientos_map:
                vencimientos_map[v.id_convenio] = v.fecha

    convs = []
    for conv in convenios:
        prox_vto = vencimientos_map.get(conv.id_convenios)
        convs.append({
            "id_convenio": conv.id_convenios,
            "monto": float(conv.importe_convenio or 0),
            "proximo_vencimiento": prox_vto.isoformat() if prox_vto else None,
        })

    # Últimos cobros (últimos 3)
    cobros = db.query(Cobro).filter(
        Cobro.cuentas_id_cta == id_cta,
        (Cobro.anulado.is_(None)) | (Cobro.anulado != "S"),
    ).order_by(Cobro.fcha_cobro.desc()).limit(3).all()

    ult_cobros = [{"fecha": c.fcha_cobro.isoformat() if c.fcha_cobro else None, "monto": float(c.importe or 0)} for c in cobros]

    return {
        "id_cta": cuenta.id_cta,
        "matricula": cuenta.entidades_matricula_ent,
        "nombre": entidad.razon_social_ent if entidad else "—",
        "deuda": float(cuenta.deudaact_cta or 0),
        "estado_id": cuenta.estados_id_estado,
        "telefonos": tels,
        "antiguedad_dias": señales["antiguedad_dias"],
        "judicial_activa": señales["judicial_activa"],
        "ultimos_contactos": ultimos_contactos,
        "convenios_activos": convs,
        "ultimos_cobros": ult_cobros,
    }


def _resumen_cartera_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Resumen de cartera: reusa smart_dash.minar_todo."""
    dias = argumentos.get("dias", 90)
    subcliente_id = argumentos.get("subcliente_id")
    estado_id = argumentos.get("estado_id")

    try:
        from src.core import smart_dash
        desde = date.today() - timedelta(days=dias)
        hasta = date.today()
        resultado = smart_dash.minar_todo(db, desde, hasta, subcliente_id, estado_id)
        return resultado
    except Exception as e:
        return {"error": str(e)}


def _top_deudores_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Top N cuentas por deuda descendente."""
    limite = min(argumentos.get("limite", 10), 20)

    cuentas = db.query(Cuenta).filter(
        Cuenta.activa_cta == "S"
    ).order_by(Cuenta.deudaact_cta.desc()).limit(limite).all()

    resultados = []
    for c in cuentas:
        resultados.append({
            "id_cta": c.id_cta,
            "matricula": c.entidades_matricula_ent,
            "nombre": c.entidad.razon_social_ent if c.entidad else "—",
            "deuda": float(c.deudaact_cta or 0),
        })

    return {"deudores": resultados}


def _gestion_periodo_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Contactos del período: reusa smart_dash.minar_gestion."""
    desde_str = argumentos.get("desde")
    hasta_str = argumentos.get("hasta")
    usuario_id = argumentos.get("usuario_id")

    if not desde_str or not hasta_str:
        return {"error": "Parámetros 'desde' y 'hasta' requeridos (formato YYYY-MM-DD)"}

    try:
        desde = datetime.fromisoformat(desde_str).date()
        hasta = datetime.fromisoformat(hasta_str).date()

        from src.core import smart_dash
        resultado = smart_dash.minar_gestion(db, desde, hasta, usuario_id=usuario_id)
        return resultado
    except Exception as e:
        return {"error": str(e)}


def _cobros_periodo_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Cobros del período: reusa smart_dash.minar_cobros."""
    desde_str = argumentos.get("desde")
    hasta_str = argumentos.get("hasta")

    if not desde_str or not hasta_str:
        return {"error": "Parámetros 'desde' y 'hasta' requeridos (formato YYYY-MM-DD)"}

    try:
        desde = datetime.fromisoformat(desde_str).date()
        hasta = datetime.fromisoformat(hasta_str).date()

        from src.core import smart_dash
        resumen = smart_dash.minar_resumen(db)
        deuda_total = float(resumen.get("deuda_total", 0))
        resultado = smart_dash.minar_cobros(db, desde, hasta, deuda_total)
        return resultado
    except Exception as e:
        return {"error": str(e)}


def _generar_informe_handler(db: Session, argumentos: dict, id_usuario: int, nombre_usuario: str | None = None) -> dict:
    """Genera informe y persiste HTML. Delega en gestor_informes.generar."""
    tipo = argumentos.get("tipo")
    parametros = argumentos.get("parametros", {})

    if tipo not in {"cuenta", "cartera", "gestion", "cobros"}:
        return {"error": f"Tipo de informe no válido: {tipo}"}

    try:
        # Import lazy: si no existe, devuelve error sin explotar
        from src.core import gestor_informes
        from src.models.gestor import GestorInforme
        import json
        from datetime import datetime

        # Llamar generar con firma correcta: (db, tipo, parametros, nombre_usuario)
        resultado = gestor_informes.generar(db, tipo, parametros, nombre_usuario or "usuario")

        # Persistir GestorInforme
        html = resultado.get("html", "")
        titulo = resultado.get("titulo", f"Informe {tipo}")

        informe = GestorInforme(
            id_usuario=id_usuario,
            tipo=tipo,
            titulo=titulo,
            parametros_json=json.dumps(parametros, default=str),
            html=html,
            creado_at=datetime.utcnow(),
            id_sesion=None
        )
        db.add(informe)
        db.flush()

        # Devuelve solo ID y título (no HTML hacia Hermes)
        return {
            "informe_id": informe.id_informe,
            "titulo": titulo,
        }
    except ImportError:
        return {"error": "Módulo gestor_informes aún no implementado"}
    except Exception as e:
        return {"error": str(e)}


def _enviar_whatsapp_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Acción: enviar WhatsApp (no se ejecuta aquí, solo valida)."""
    # Esta es una acción, no se ejecuta en el loop de tools
    return {"error": "Acción pendiente de confirmación"}


def _crear_agenda_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Acción: crear agenda (no se ejecuta aquí, solo valida)."""
    return {"error": "Acción pendiente de confirmación"}


def _registrar_contacto_handler(db: Session, argumentos: dict, id_usuario: int) -> dict:
    """Acción: registrar contacto (no se ejecuta aquí, solo valida)."""
    return {"error": "Acción pendiente de confirmación"}


# Registro de tools: (schema, handler)
_TOOLS = {
    "buscar_cuentas": (
        {
            "type": "function",
            "function": {
                "name": "buscar_cuentas",
                "description": "Busca cuentas por matrícula, nombre o ID. Retorna lista con deuda y estado.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "Término de búsqueda (matrícula, nombre parcial o id_cta)",
                        },
                        "limite": {
                            "type": "integer",
                            "description": "Máximo de resultados (default 10, máximo 20)",
                            "default": 10,
                        },
                    },
                    "required": ["q"],
                },
            },
        },
        _buscar_cuentas_handler,
    ),
    "dossier_cuenta": (
        {
            "type": "function",
            "function": {
                "name": "dossier_cuenta",
                "description": "Dossier completo de una cuenta: deuda, teléfonos, señales, últimos contactos, convenios, cobros.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id_cta": {
                            "type": "integer",
                            "description": "ID de la cuenta",
                        },
                    },
                    "required": ["id_cta"],
                },
            },
        },
        _dossier_cuenta_handler,
    ),
    "resumen_cartera": (
        {
            "type": "function",
            "function": {
                "name": "resumen_cartera",
                "description": "Resumen agregado de cartera: total de cuentas, deuda total, aging, concentración.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dias": {
                            "type": "integer",
                            "description": "Período de análisis en días (default 90)",
                            "default": 90,
                        },
                        "subcliente_id": {
                            "type": "integer",
                            "description": "Filtrar por subcliente (opcional)",
                        },
                        "estado_id": {
                            "type": "integer",
                            "description": "Filtrar por estado (opcional)",
                        },
                    },
                },
            },
        },
        _resumen_cartera_handler,
    ),
    "top_deudores": (
        {
            "type": "function",
            "function": {
                "name": "top_deudores",
                "description": "Top N cuentas por deuda descendente.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limite": {
                            "type": "integer",
                            "description": "Cantidad de deudores (default 10, máximo 20)",
                            "default": 10,
                        },
                    },
                },
            },
        },
        _top_deudores_handler,
    ),
    "gestion_periodo": (
        {
            "type": "function",
            "function": {
                "name": "gestion_periodo",
                "description": "Análisis de gestión en un período: contactos, acciones, resultados.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "desde": {
                            "type": "string",
                            "description": "Fecha inicial (formato YYYY-MM-DD)",
                        },
                        "hasta": {
                            "type": "string",
                            "description": "Fecha final (formato YYYY-MM-DD)",
                        },
                        "usuario_id": {
                            "type": "integer",
                            "description": "Filtrar por usuario (opcional)",
                        },
                    },
                    "required": ["desde", "hasta"],
                },
            },
        },
        _gestion_periodo_handler,
    ),
    "cobros_periodo": (
        {
            "type": "function",
            "function": {
                "name": "cobros_periodo",
                "description": "Cobros realizados en un período: detalle y totales.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "desde": {
                            "type": "string",
                            "description": "Fecha inicial (formato YYYY-MM-DD)",
                        },
                        "hasta": {
                            "type": "string",
                            "description": "Fecha final (formato YYYY-MM-DD)",
                        },
                    },
                    "required": ["desde", "hasta"],
                },
            },
        },
        _cobros_periodo_handler,
    ),
    "generar_informe": (
        {
            "type": "function",
            "function": {
                "name": "generar_informe",
                "description": "Genera un informe descargable en PDF/planilla. Tipos: cuenta, cartera, gestion, cobros.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tipo": {
                            "type": "string",
                            "description": "Tipo de informe: cuenta, cartera, gestion, cobros",
                            "enum": ["cuenta", "cartera", "gestion", "cobros"],
                        },
                        "parametros": {
                            "type": "object",
                            "description": (
                                "Parámetros exactos según 'tipo': "
                                "cuenta -> {id_cta: int (requerido)}; "
                                "cartera -> {dias?: int (default 90), desde?: 'YYYY-MM-DD', hasta?: 'YYYY-MM-DD', subcliente_id?: int, estado_id?: int}; "
                                "gestion -> {desde: 'YYYY-MM-DD' (requerido), hasta: 'YYYY-MM-DD' (requerido), usuario_id?: int}; "
                                "cobros -> {desde: 'YYYY-MM-DD' (requerido), hasta: 'YYYY-MM-DD' (requerido)}."
                            ),
                        },
                    },
                    "required": ["tipo"],
                },
            },
        },
        _generar_informe_handler,
    ),
    "enviar_whatsapp": (
        {
            "type": "function",
            "function": {
                "name": "enviar_whatsapp",
                "description": "REQUIERE CONFIRMACIÓN: envía mensaje WhatsApp a una cuenta.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id_cta": {
                            "type": "integer",
                            "description": "ID de la cuenta",
                        },
                        "telefono": {
                            "type": "string",
                            "description": "Número de teléfono",
                        },
                        "tipo_mensaje": {
                            "type": "string",
                            "description": "Tipo de plantilla (recordatorio, oferta, etc.)",
                        },
                    },
                    "required": ["id_cta", "telefono", "tipo_mensaje"],
                },
            },
        },
        _enviar_whatsapp_handler,
    ),
    "crear_agenda": (
        {
            "type": "function",
            "function": {
                "name": "crear_agenda",
                "description": "REQUIERE CONFIRMACIÓN: crea un evento de seguimiento en la agenda.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id_cta": {
                            "type": "integer",
                            "description": "ID de la cuenta",
                        },
                        "fecha": {
                            "type": "string",
                            "description": "Fecha del evento (YYYY-MM-DD)",
                        },
                        "hora": {
                            "type": "string",
                            "description": "Hora del evento (HH:MM)",
                        },
                        "nota": {
                            "type": "string",
                            "description": "Nota o descripción del seguimiento",
                        },
                    },
                    "required": ["id_cta", "fecha"],
                },
            },
        },
        _crear_agenda_handler,
    ),
    "registrar_contacto": (
        {
            "type": "function",
            "function": {
                "name": "registrar_contacto",
                "description": "REQUIERE CONFIRMACIÓN: registra un contacto (llamada, WhatsApp, etc.) sobre una cuenta.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id_cta": {
                            "type": "integer",
                            "description": "ID de la cuenta",
                        },
                        "accion_id": {
                            "type": "integer",
                            "description": "ID de la acción realizada",
                        },
                        "resultado_id": {
                            "type": "integer",
                            "description": "ID del resultado del contacto",
                        },
                        "nota": {
                            "type": "string",
                            "description": "Nota del contacto",
                        },
                    },
                    "required": ["id_cta", "accion_id", "resultado_id"],
                },
            },
        },
        _registrar_contacto_handler,
    ),
}

# Exportar schemas derivados de _TOOLS
TOOLS_SCHEMA = [schema for schema, _ in _TOOLS.values()]


def ejecutar_tool(db: Session, nombre: str, argumentos: dict, id_usuario: int, nombre_usuario: str | None = None) -> dict:
    """
    Ejecuta una tool por nombre.

    Retorna siempre un dict JSON-serializable.
    - Tools de lectura: ejecución inmediata.
    - Tools de acción: devuelven {"error": "Acción pendiente de confirmación"}.
    - Tool desconocida: {"error": "tool desconocida: X"}.

    Nunca lanza excepción.
    """
    if nombre not in _TOOLS:
        return {"error": f"tool desconocida: {nombre}"}

    try:
        schema, handler = _TOOLS[nombre]
        # Pasar nombre_usuario si el handler es generar_informe
        if nombre == "generar_informe":
            resultado = handler(db, argumentos, id_usuario, nombre_usuario)
        else:
            resultado = handler(db, argumentos, id_usuario)
        return resultado
    except Exception as e:
        return {"error": str(e)}
