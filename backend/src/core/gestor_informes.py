"""
Chat-Cobranza: generación de informes HTML + hojas xlsx.

Funciones puras _render_* que generan HTML autocontenido (A4-friendly).
Función generar que consulta DB y delega render.
Función a_dataframes que convierte datos a dict de DataFrames para xlsx.
"""

from datetime import date, datetime, timedelta
from typing import Dict
import pandas as pd
from sqlalchemy.orm import Session

from src.core import smart_dash


TEMPLATE_BASE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page {{ size: A4; margin: 2cm; }}
body {{ font-family: Arial, sans-serif; font-size: 11pt; color: #333; }}
h1 {{ color: #1a1a1a; margin-bottom: 0.5cm; font-size: 18pt; }}
h2 {{ color: #0066cc; margin-top: 1cm; margin-bottom: 0.3cm; font-size: 13pt; border-bottom: 1pt solid #ccc; padding-bottom: 0.2cm; }}
table {{ width: 100%; border-collapse: collapse; margin: 0.5cm 0; }}
table th {{ background-color: #0066cc; color: white; padding: 0.4cm; text-align: left; font-weight: bold; }}
table td {{ padding: 0.3cm; border-bottom: 1pt solid #eee; }}
table tr:nth-child(even) {{ background-color: #f9f9f9; }}
.header {{ text-align: center; margin-bottom: 1cm; border-bottom: 2pt solid #0066cc; padding-bottom: 0.5cm; }}
.header-info {{ font-size: 10pt; color: #666; margin-top: 0.3cm; }}
.footer {{ text-align: center; font-size: 9pt; color: #999; margin-top: 1cm; padding-top: 0.5cm; border-top: 1pt solid #ccc; page-break-after: always; }}
.numero {{ text-align: right; }}
.hallazgo {{ margin: 0.5cm 0; padding: 0.4cm; border-left: 3pt solid #0066cc; background-color: #f0f5ff; }}
.hallazgo.critico {{ border-left-color: #d32f2f; background-color: #ffebee; }}
.hallazgo.atencion {{ border-left-color: #f57c00; background-color: #fff3e0; }}
.hallazgo.positivo {{ border-left-color: #388e3c; background-color: #e8f5e9; }}
.hallazgo-titulo {{ font-weight: bold; color: #1a1a1a; margin-bottom: 0.2cm; }}
.hallazgo-detalle {{ font-size: 10pt; color: #555; }}
</style>
</head>
<body>
{header}
{contenido}
{footer}
</body>
</html>
"""


def _fmt_monto(valor: float) -> str:
    """Formatea valor numérico como moneda."""
    return f"$ {valor:,.0f}".replace(",", ".")


def _render_cuenta(datos: dict, nombre_usuario: str, fecha: date) -> str:
    """Render puro de informe de cuenta."""
    id_cta = datos.get("id_cta", "—")
    matricula = datos.get("matricula", "—")
    nombre = datos.get("nombre", "—")
    deuda = datos.get("deuda", 0.0)

    header = f"""
    <div class="header">
        <h1>Dossier de Cuenta</h1>
        <div class="header-info">
            <p><strong>Cuenta:</strong> {id_cta} | <strong>Matrícula:</strong> {matricula} | <strong>Cliente:</strong> {nombre}</p>
            <p><strong>Fecha:</strong> {fecha.strftime('%d/%m/%Y')} | <strong>Deuda actual:</strong> {_fmt_monto(deuda)}</p>
        </div>
    </div>
    """

    contenido = f"""
    <h2>Información General</h2>
    <table>
        <tr><th>Campo</th><th>Valor</th></tr>
        <tr><td>ID Cuenta</td><td>{id_cta}</td></tr>
        <tr><td>Matrícula</td><td>{matricula}</td></tr>
        <tr><td>Nombre</td><td>{nombre}</td></tr>
        <tr><td>Deuda Actual</td><td class="numero">{_fmt_monto(deuda)}</td></tr>
    </table>
    """

    footer = f'<div class="footer">Generado por Chat-Cobranza — {nombre_usuario} — {fecha.strftime("%d/%m/%Y %H:%M")}</div>'

    return TEMPLATE_BASE.format(header=header, contenido=contenido, footer=footer)


def _render_cartera(datos: dict, nombre_usuario: str, fecha: date) -> str:
    """Render puro de informe de cartera."""
    resumen = datos.get("resumen", {})
    aging = datos.get("aging", [])
    conc = datos.get("concentracion", {})
    hallazgos = datos.get("hallazgos", [])

    total = resumen.get("total", 0)
    deuda_total = resumen.get("deuda_total", 0.0)
    deuda_prom = resumen.get("deuda_promedio", 0.0)

    header = f"""
    <div class="header">
        <h1>Informe de Cartera</h1>
        <div class="header-info">
            <p><strong>Total Cuentas:</strong> {total} | <strong>Deuda Total:</strong> {_fmt_monto(deuda_total)}</p>
            <p><strong>Fecha:</strong> {fecha.strftime('%d/%m/%Y')}</p>
        </div>
    </div>
    """

    # Resumen
    contenido = f"""
    <h2>Resumen Ejecutivo</h2>
    <table>
        <tr><th>Métrica</th><th>Valor</th></tr>
        <tr><td>Total de Cuentas</td><td class="numero">{total}</td></tr>
        <tr><td>Deuda Total</td><td class="numero">{_fmt_monto(deuda_total)}</td></tr>
        <tr><td>Deuda Promedio</td><td class="numero">{_fmt_monto(deuda_prom)}</td></tr>
    </table>

    <h2>Aging de Cartera</h2>
    <table>
        <tr><th>Bucket</th><th>Cuentas</th><th>Deuda</th></tr>
    """

    for bucket in aging:
        nombre_bucket = bucket.get("bucket", "—")
        cuentas = bucket.get("cuentas", 0)
        deuda = bucket.get("deuda", 0.0)
        contenido += f"<tr><td>{nombre_bucket}</td><td class='numero'>{cuentas}</td><td class='numero'>{_fmt_monto(deuda)}</td></tr>"

    contenido += """
    </table>

    <h2>Concentración de Deuda</h2>
    <table>
        <tr><th>Métrica</th><th>Valor</th></tr>
    """

    top_cuentas = conc.get("top_cuentas", 0)
    deuda_top = conc.get("deuda_top", 0.0)
    porcentaje = conc.get("porcentaje", 0.0)

    contenido += f"""
        <tr><td>Top Cuentas</td><td class="numero">{top_cuentas}</td></tr>
        <tr><td>Deuda Top</td><td class="numero">{_fmt_monto(deuda_top)}</td></tr>
        <tr><td>Porcentaje</td><td class="numero">{porcentaje:.1f}%</td></tr>
    </table>
    """

    # Hallazgos
    if hallazgos:
        contenido += "<h2>Hallazgos</h2>"
        for h in hallazgos:
            nivel = h.get("nivel", "info")
            titulo = h.get("titulo", "—")
            detalle = h.get("detalle", "—")
            contenido += f'''
    <div class="hallazgo {nivel}">
        <div class="hallazgo-titulo">{titulo}</div>
        <div class="hallazgo-detalle">{detalle}</div>
    </div>
    '''

    footer = f'<div class="footer">Generado por Chat-Cobranza — {nombre_usuario} — {fecha.strftime("%d/%m/%Y %H:%M")}</div>'

    return TEMPLATE_BASE.format(header=header, contenido=contenido, footer=footer)


def _render_gestion(datos: dict, desde: date, hasta: date, nombre_usuario: str, fecha: date) -> str:
    """Render puro de informe de gestión."""
    contactos = datos.get("contactos", 0)
    por_accion = datos.get("por_accion", [])
    por_resultado = datos.get("por_resultado", [])
    tasa_compromiso = datos.get("tasa_compromiso", 0.0)
    sin_gestion = datos.get("sin_gestion_30d", 0)

    header = f"""
    <div class="header">
        <h1>Informe de Gestión de Cobranza</h1>
        <div class="header-info">
            <p><strong>Período:</strong> {desde.strftime('%d/%m/%Y')} a {hasta.strftime('%d/%m/%Y')}</p>
            <p><strong>Contactos Realizados:</strong> {contactos}</p>
        </div>
    </div>
    """

    contenido = f"""
    <h2>Resumen de Actividad</h2>
    <table>
        <tr><th>Métrica</th><th>Valor</th></tr>
        <tr><td>Total Contactos</td><td class="numero">{contactos}</td></tr>
        <tr><td>Tasa Compromiso</td><td class="numero">{tasa_compromiso:.1f}%</td></tr>
        <tr><td>Sin Gestión 30d</td><td class="numero">{sin_gestion}</td></tr>
    </table>

    <h2>Por Acción</h2>
    <table>
        <tr><th>Acción</th><th>Cantidad</th></tr>
    """

    for accion in por_accion:
        desc = accion.get("desc", "—")
        cant = accion.get("cant", 0)
        contenido += f"<tr><td>{desc}</td><td class='numero'>{cant}</td></tr>"

    contenido += """
    </table>

    <h2>Por Resultado</h2>
    <table>
        <tr><th>Resultado</th><th>Cantidad</th></tr>
    """

    for res in por_resultado:
        desc = res.get("desc", "—")
        cant = res.get("cant", 0)
        contenido += f"<tr><td>{desc}</td><td class='numero'>{cant}</td></tr>"

    contenido += "</table>"

    footer = f'<div class="footer">Generado por Chat-Cobranza — {nombre_usuario} — {fecha.strftime("%d/%m/%Y %H:%M")}</div>'

    return TEMPLATE_BASE.format(header=header, contenido=contenido, footer=footer)


def _render_cobros(datos: dict, desde: date, hasta: date, nombre_usuario: str, fecha: date) -> str:
    """Render puro de informe de cobros."""
    por_mes = datos.get("por_mes", [])
    tendencia = datos.get("tendencia_pct", None)
    recuperado = datos.get("recuperado", 0.0)
    pct_recuperado = datos.get("pct_recuperado", 0.0)

    header = f"""
    <div class="header">
        <h1>Informe de Cobros</h1>
        <div class="header-info">
            <p><strong>Período:</strong> {desde.strftime('%d/%m/%Y')} a {hasta.strftime('%d/%m/%Y')}</p>
            <p><strong>Recuperado:</strong> {_fmt_monto(recuperado)} ({pct_recuperado:.1f}%)</p>
        </div>
    </div>
    """

    contenido = f"""
    <h2>Resumen de Recaudación</h2>
    <table>
        <tr><th>Métrica</th><th>Valor</th></tr>
        <tr><td>Total Recuperado</td><td class="numero">{_fmt_monto(recuperado)}</td></tr>
        <tr><td>Porcentaje</td><td class="numero">{pct_recuperado:.1f}%</td></tr>
    """

    if tendencia is not None:
        contenido += f"<tr><td>Tendencia</td><td class='numero'>{tendencia:+.1f}%</td></tr>"

    contenido += """
    </table>

    <h2>Cobros por Mes</h2>
    <table>
        <tr><th>Mes</th><th>Importe</th></tr>
    """

    for mes_data in por_mes:
        mes = mes_data.get("mes", "—")
        importe = mes_data.get("importe", 0.0)
        contenido += f"<tr><td>{mes}</td><td class='numero'>{_fmt_monto(importe)}</td></tr>"

    contenido += "</table>"

    footer = f'<div class="footer">Generado por Chat-Cobranza — {nombre_usuario} — {fecha.strftime("%d/%m/%Y %H:%M")}</div>'

    return TEMPLATE_BASE.format(header=header, contenido=contenido, footer=footer)


def a_dataframes(tipo: str, datos: dict) -> Dict[str, pd.DataFrame]:
    """
    Convierte datos a dict de DataFrames (hojas para xlsx).

    Para cartera: Resumen, Aging, Concentración.
    Para otros tipos: DataFrame único.
    """
    if tipo == "cartera":
        dfs = {}

        # Hoja Resumen
        resumen = datos.get("resumen", {})
        df_resumen = pd.DataFrame([
            {"Métrica": "Total Cuentas", "Valor": resumen.get("total", 0)},
            {"Métrica": "Deuda Total", "Valor": resumen.get("deuda_total", 0.0)},
            {"Métrica": "Deuda Promedio", "Valor": resumen.get("deuda_promedio", 0.0)},
            {"Métrica": "Deuda Máxima", "Valor": resumen.get("deuda_max", 0.0)},
        ])
        dfs["Resumen"] = df_resumen

        # Hoja Aging
        aging = datos.get("aging", [])
        df_aging = pd.DataFrame(aging)
        dfs["Aging"] = df_aging

        # Hoja Concentración
        conc = datos.get("concentracion", {})
        df_conc = pd.DataFrame([
            {"Métrica": "Top Cuentas", "Valor": conc.get("top_cuentas", 0)},
            {"Métrica": "Deuda Top", "Valor": conc.get("deuda_top", 0.0)},
            {"Métrica": "Porcentaje", "Valor": conc.get("porcentaje", 0.0)},
        ])
        dfs["Concentración"] = df_conc

        return dfs

    elif tipo == "gestion":
        df = pd.DataFrame({
            "Métrica": [
                "Contactos",
                "Tasa Compromiso",
                "Sin Gestión 30d",
            ],
            "Valor": [
                datos.get("contactos", 0),
                datos.get("tasa_compromiso", 0.0),
                datos.get("sin_gestion_30d", 0),
            ],
        })
        return {"Gestión": df}

    elif tipo == "cobros":
        por_mes = datos.get("por_mes", [])
        df = pd.DataFrame(por_mes)
        return {"Cobros": df}

    elif tipo == "cuenta":
        df = pd.DataFrame({
            "Campo": [
                "ID Cuenta",
                "Matrícula",
                "Nombre",
                "Deuda",
            ],
            "Valor": [
                datos.get("id_cta", "—"),
                datos.get("matricula", "—"),
                datos.get("nombre", "—"),
                datos.get("deuda", 0.0),
            ],
        })
        return {"Cuenta": df}

    else:
        raise ValueError(f"Tipo de informe no válido: {tipo}")


def generar(db: Session, tipo: str, parametros: dict, nombre_usuario: str) -> dict:
    """
    Genera informe completo (HTML + datos).

    Parámetros esperados por tipo:
    - cuenta: {id_cta}
    - cartera: {dias?, desde?, hasta?, subcliente_id?, estado_id?}
    - gestion: {desde, hasta, usuario_id?}
    - cobros: {desde, hasta}

    Retorna:
        {
            "titulo": str,
            "html": str (autocontenido, A4-friendly),
            "datos": dict (datos estructura usada en render)
        }

    Raises:
        ValueError si tipo no es válido.
    """
    tipos_validos = {"cuenta", "cartera", "gestion", "cobros"}
    if tipo not in tipos_validos:
        raise ValueError(f"Tipo de informe no válido: {tipo}. Esperados: {tipos_validos}")

    hoy = date.today()
    ahora = datetime.now()

    if tipo == "cuenta":
        id_cta = parametros.get("id_cta")
        if not id_cta:
            raise ValueError("Parámetro 'id_cta' requerido para tipo 'cuenta'")

        # Reusa patrón dossier de gestor_tools
        from src.models.cuentas import Cuenta, Entidad
        from src.models.contactos import Telefono, Agenda
        from src.models.financiero import Convenio, Vencimiento, Cobro
        from src.models.judicial import Demanda
        from src.models.catalogos import Accion, Resultado

        cuenta = db.query(Cuenta).filter(Cuenta.id_cta == id_cta).first()
        if not cuenta:
            raise ValueError(f"Cuenta {id_cta} no encontrada")

        entidad = db.query(Entidad).filter(Entidad.matricula_ent == cuenta.entidades_matricula_ent).first()

        datos = {
            "id_cta": cuenta.id_cta,
            "matricula": cuenta.entidades_matricula_ent,
            "nombre": entidad.razon_social_ent if entidad else "—",
            "deuda": float(cuenta.deudaact_cta or 0),
        }

        titulo = f"Dossier - {datos['nombre']} (Cta. {id_cta})"
        html = _render_cuenta(datos, nombre_usuario, hoy)

    elif tipo == "cartera":
        dias = parametros.get("dias", 90)
        desde = parametros.get("desde")
        hasta = parametros.get("hasta")
        subcliente_id = parametros.get("subcliente_id")
        estado_id = parametros.get("estado_id")

        if desde:
            desde = datetime.fromisoformat(desde).date() if isinstance(desde, str) else desde
        else:
            desde = hoy - timedelta(days=dias)

        if hasta:
            hasta = datetime.fromisoformat(hasta).date() if isinstance(hasta, str) else hasta
        else:
            hasta = hoy

        datos = smart_dash.minar_todo(db, desde, hasta, subcliente_id, estado_id)

        # Generar hallazgos
        hallazgos = smart_dash.generar_hallazgos(datos)
        datos["hallazgos"] = hallazgos

        titulo = f"Cartera - {desde.strftime('%d/%m/%Y')} a {hasta.strftime('%d/%m/%Y')}"
        html = _render_cartera(datos, nombre_usuario, hoy)

    elif tipo == "gestion":
        desde_str = parametros.get("desde")
        hasta_str = parametros.get("hasta")
        usuario_id = parametros.get("usuario_id")

        if not desde_str or not hasta_str:
            raise ValueError("Parámetros 'desde' y 'hasta' requeridos para tipo 'gestion'")

        desde = datetime.fromisoformat(desde_str).date() if isinstance(desde_str, str) else desde_str
        hasta = datetime.fromisoformat(hasta_str).date() if isinstance(hasta_str, str) else hasta_str

        datos = smart_dash.minar_gestion(db, desde, hasta, usuario_id=usuario_id)

        titulo = f"Gestión - {desde.strftime('%d/%m/%Y')} a {hasta.strftime('%d/%m/%Y')}"
        html = _render_gestion(datos, desde, hasta, nombre_usuario, hoy)

    elif tipo == "cobros":
        desde_str = parametros.get("desde")
        hasta_str = parametros.get("hasta")

        if not desde_str or not hasta_str:
            raise ValueError("Parámetros 'desde' y 'hasta' requeridos para tipo 'cobros'")

        desde = datetime.fromisoformat(desde_str).date() if isinstance(desde_str, str) else desde_str
        hasta = datetime.fromisoformat(hasta_str).date() if isinstance(hasta_str, str) else hasta_str

        # Para cobros necesitamos deuda_total
        resumen = smart_dash.minar_resumen(db)
        deuda_total = resumen.get("deuda_total", 0.0)

        datos = smart_dash.minar_cobros(db, desde, hasta, deuda_total)

        titulo = f"Cobros - {desde.strftime('%d/%m/%Y')} a {hasta.strftime('%d/%m/%Y')}"
        html = _render_cobros(datos, desde, hasta, nombre_usuario, hoy)

    return {
        "titulo": titulo,
        "html": html,
        "datos": datos,
    }
