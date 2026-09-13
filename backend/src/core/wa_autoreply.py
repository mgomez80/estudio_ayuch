"""
Auto-respuesta automática 24h para WhatsApp.

Chequea si un teléfono puede recibir auto-respuesta (máx 1 cada 24h),
matchea keywords contra el texto entrante, y registra el envío en DB.
"""

from datetime import datetime, timedelta
from sqlalchemy import text


# Keywords y sus respuestas (rioplatense, placeholders genéricos)
KEYWORDS_RESPUESTAS = {
    "hola": "¡Hola! Un gestor te va a contactar a la brevedad.",
    "buenos": "¡Hola! Nos alegra tu mensaje. Un gestor te va a contactar a la brevedad.",
    "turno": "Para gestionar tu turno, un ejecutivo se va a poner en contacto con vos.",
    "cita": "Para agendar tu cita, un ejecutivo se va a poner en contacto con vos.",
    "gracias": "¡Gracias por tu confianza! Un gestor te va a contactar a la brevedad.",
}


def puede_autoresponder(db, telefono: str) -> bool:
    """
    Chequea si un teléfono puede recibir auto-respuesta.
    True si: nunca se respondió automáticamente, o pasaron >= 24h.
    """
    query = text(
        "SELECT MAX(ultimo_envio) FROM whatsapp_autoreply_control WHERE telefono = :tel"
    )
    result = db.execute(query, {"tel": telefono}).scalar()

    if result is None:
        # Nunca se respondió automáticamente
        return True

    # Chequear si pasaron >= 24h
    hace_24h = datetime.now() - timedelta(hours=24)
    return result < hace_24h


def generar_autorespuesta(texto_entrante: str) -> str | None:
    """
    Matchea keywords contra el texto (case-insensitive) y devuelve
    la respuesta automática correspondiente, o None si no aplica.
    """
    if not texto_entrante:
        return None

    texto_lower = texto_entrante.lower()

    for keyword, respuesta in KEYWORDS_RESPUESTAS.items():
        if keyword in texto_lower:
            return respuesta

    return None


def registrar_autorespuesta(db, telefono: str) -> None:
    """
    UPSERT en whatsapp_autoreply_control: registra/actualiza el último
    envío automático y cuenta de auto-respuestas.
    """
    query = text(
        """
        INSERT INTO whatsapp_autoreply_control (telefono, ultimo_envio, veces)
        VALUES (:tel, :ahora, 1)
        ON DUPLICATE KEY UPDATE
            ultimo_envio = :ahora,
            veces = veces + 1
        """
    )
    db.execute(query, {"tel": telefono, "ahora": datetime.now()})
