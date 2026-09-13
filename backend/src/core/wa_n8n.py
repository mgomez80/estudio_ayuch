import re

import httpx
from pydantic_settings import BaseSettings


class WaSettings(BaseSettings):
    n8n_wa_webhook_url: str = ""
    n8n_wa_adjunto_webhook_url: str = ""
    ycloud_from: str = ""
    wa_max_mensajes_dia: int = 500
    wa_delay_mensajes: int = 5
    wa_delay_lote: int = 60
    wa_tam_lote: int = 20
    wa_max_reintentos: int = 3
    wa_delay_reintento: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


wa_settings = WaSettings()


# Debe coincidir exacto con templateVars del nodo "Preparar datos" en n8n.
TEMPLATE_VARS = {
    "aviso_opciones_pago_estudio_lg": ["nombre", "cliente"],
    "aviso_saldo_pendiente_estudio_lg": ["nombre", "cliente"],
    "aviso_gestion_juridica_estudio_lg": ["nombre", "cliente"],
    "aviso_cesion_credito_estudio_lg": ["nombre", "cliente"],
}


def normalizar_telefono(numero: str) -> str:
    """Normaliza un teléfono a formato internacional WhatsApp.
    Sin prefijo de país asume Argentina: 549 + area + numero.
    Port de normalizarTelefono() del legacy PHP (con fix código país '1')."""
    n = re.sub(r"\D+", "", str(numero or ""))
    if not n:
        return ""

    if n.startswith("00"):
        n = n[2:]
    if n.startswith("0"):
        n = n.lstrip("0")
    if not n:
        return ""

    if n.startswith("54"):
        resto = n[2:]
        if not resto.startswith("9"):
            n = "549" + resto
        return n

    # '1' (EEUU/Canadá) solo con 11+ dígitos; "11..." de 10 dígitos es CABA.
    if n.startswith("1") and len(n) >= 11:
        return n
    otros_paises = ["52", "55", "56", "57", "58", "51", "591", "593", "595", "598"]
    for cc in otros_paises:
        if n.startswith(cc) and len(n) >= 10:
            return n

    if n.startswith("15") and len(n) > 8:
        n = n[2:]
    return "549" + n


def enviar_plantilla(telefono: str, nombre: str, cliente: str,
                     mensaje: str, template_name: str, gestor: str = "") -> dict:
    """POST al webhook n8n con plantilla Meta + variables (mismo payload que
    envio_post_n8n.php). El mensaje renderizado viaja solo para log del workflow;
    n8n arma el mensaje real con la plantilla aprobada. Simula si no hay URL."""
    url = wa_settings.n8n_wa_webhook_url
    if not url or url == "CHANGEME":
        print(f"[WA N8N SIMULADO] {template_name} -> {telefono} ({nombre}/{cliente})")
        return {"ok": True, "estado": "simulado", "detalle": None, "ycloud_id": None}

    data = {
        "phone": telefono, "to": telefono, "number": telefono,
        "nombre": nombre, "cliente": cliente, "gestor": gestor,
        "mensaje": mensaje, "templateName": template_name,
        "from": wa_settings.ycloud_from,
    }
    try:
        resp = httpx.post(url, json=data,
                          headers={"Content-Type": "application/json", "Accept": "application/json"},
                          timeout=30)
    except Exception as e:
        return {"ok": False, "estado": "fallido", "detalle": f"CURL: {e}", "ycloud_id": None}

    if not (200 <= resp.status_code < 300):
        return {"ok": False, "estado": "fallido", "detalle": f"HTTP {resp.status_code}", "ycloud_id": None}

    try:
        body = resp.json()
    except Exception:
        body = None
    if isinstance(body, dict):
        if body.get("error"):
            return {"ok": False, "estado": "fallido", "detalle": str(body["error"]), "ycloud_id": None}
        if body.get("success") is False:
            return {"ok": False, "estado": "fallido",
                    "detalle": str(body.get("message", "Error interno del webhook")), "ycloud_id": None}
    ycloud_id = body.get("id") or None if isinstance(body, dict) else None
    return {"ok": True, "estado": "enviado", "detalle": None, "ycloud_id": ycloud_id}


def armar_parametros_plantilla(template_name: str, valores: dict) -> list[dict]:
    """Arma la lista de parámetros posicionales para una plantilla Meta.

    Valida que:
    - La plantilla esté registrada en TEMPLATE_VARS.
    - Todos los valores requeridos estén presentes y sean truthy.

    Devuelve lista de dicts con type='text' y el text de cada variable en orden.
    Lanza ValueError si faltan datos o la plantilla no existe.
    """
    if template_name not in TEMPLATE_VARS:
        raise ValueError(
            f'Plantilla "{template_name}" no registrada en TEMPLATE_VARS. '
            f"Registrala con su orden de variables antes de enviar."
        )

    orden = TEMPLATE_VARS[template_name]
    faltantes = [v for v in orden if not valores.get(v)]
    if faltantes:
        raise ValueError(
            f"Faltan [{', '.join(faltantes)}] para {template_name}. "
            f"Espera {len(orden)} variables en orden: {', '.join(orden)}."
        )

    return [{"type": "text", "text": valores[v]} for v in orden]
