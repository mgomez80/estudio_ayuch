"""Cliente SMTP para envío de mail (individual y masivo).
Sin SMTP_HOST operá en modo simulado (desarrollo sin credenciales)."""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic_settings import BaseSettings

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class MailSettings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""
    smtp_from_nombre: str = "Estudio Lino Gonzalez"
    smtp_use_tls: bool = True
    mail_max_dia: int = 500
    mail_delay_mensajes: int = 2
    mail_delay_lote: int = 30
    mail_tam_lote: int = 30
    mail_max_reintentos: int = 3
    mail_delay_reintento: int = 15


mail_settings = MailSettings()


def validar_email(direccion: str) -> str:
    """Normaliza (trim/lower) y valida formato básico. Devuelve '' si inválido."""
    d = (direccion or "").strip().lower()
    return d if EMAIL_RE.match(d) else ""


def enviar_mail(destino: str, asunto: str, cuerpo: str) -> dict:
    """Envía un mail por SMTP. Simula si no hay SMTP_HOST configurado (mismo
    patrón que enviar_plantilla() en wa_n8n.py para WhatsApp)."""
    if not mail_settings.smtp_host:
        print(f"[MAIL SIMULADO] {asunto!r} -> {destino}")
        return {"ok": True, "estado": "simulado", "detalle": None}

    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    remitente = f"{mail_settings.smtp_from_nombre} <{mail_settings.smtp_from}>" if mail_settings.smtp_from_nombre else mail_settings.smtp_from
    msg["From"] = remitente
    msg["To"] = destino
    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        with smtplib.SMTP(mail_settings.smtp_host, mail_settings.smtp_port, timeout=30) as server:
            if mail_settings.smtp_use_tls:
                server.starttls()
            if mail_settings.smtp_user:
                server.login(mail_settings.smtp_user, mail_settings.smtp_password)
            server.sendmail(mail_settings.smtp_from, [destino], msg.as_string())
    except Exception as e:
        return {"ok": False, "estado": "fallido", "detalle": str(e)}

    return {"ok": True, "estado": "enviado", "detalle": None}
