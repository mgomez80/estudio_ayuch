import random
import time
from datetime import datetime

from src.core.auth_database import AuthSessionLocal
from src.core.database import SessionLocal
from src.core.mail_sender import enviar_mail, mail_settings
from src.core.mail_registro import conteo_diario_mail, registrar_contacto_mail, registrar_envio_mail
from src.core.wa_registro import render_texto
from src.models.mail import MailEnvioMasivo
from src.models.usuario import Usuario


def recortar_por_limite(destinatarios: list, ya_enviados_hoy: int, maximo: int) -> list:
    restante = max(0, maximo - ya_enviados_hoy)
    return destinatarios[:restante]


def procesar_envio_masivo_mail(id_envio: int, destinatarios: list[dict],
                               plantilla: dict, id_usuario: int) -> None:
    """Worker background: itera destinatarios con delays anti-bloqueo y
    reintentos; actualiza el job y el log. Nunca lanza (job queda 'error')."""
    db = SessionLocal()
    try:
        job = db.query(MailEnvioMasivo).filter(MailEnvioMasivo.id_envio == id_envio).first()
        if not job:
            return
        job.estado = "en_curso"
        db.commit()

        auth_db = AuthSessionLocal()
        try:
            usuario = (auth_db.query(Usuario.loguin_usuario, Usuario.nombre_completo)
                       .filter(Usuario.id_usuario == id_usuario).first())
        finally:
            auth_db.close()
        gestor = (usuario.nombre_completo or usuario.loguin_usuario) if usuario else "Estudio Lino Gonzalez"

        lote = recortar_por_limite(
            destinatarios, conteo_diario_mail(db, id_usuario), mail_settings.mail_max_dia
        )
        recortados = len(destinatarios) - len(lote)
        if recortados:
            job.errores += recortados
            for d in destinatarios[len(lote):]:
                registrar_envio_mail(db, matricula=d["matricula"], id_cta=d.get("id_cta"),
                                     destino=d["email"], asunto=plantilla["asunto"], mensaje="",
                                     tipo=plantilla["id"], id_usuario=id_usuario,
                                     estado="DESCARTADO: limite diario", envio_masivo_id=id_envio)
            db.commit()

        for idx, d in enumerate(lote):
            texto = render_texto(plantilla["texto"], d.get("nombre"), d.get("cliente"), gestor)
            asunto = render_texto(plantilla["asunto"], d.get("nombre"), d.get("cliente"), gestor)

            resultado = None
            for intento in range(1, mail_settings.mail_max_reintentos + 1):
                resultado = enviar_mail(d["email"], asunto, texto)
                if resultado["ok"]:
                    break
                if intento < mail_settings.mail_max_reintentos:
                    time.sleep(mail_settings.mail_delay_reintento)

            if resultado["ok"]:
                job.enviados += 1
                registrar_envio_mail(db, matricula=d["matricula"], id_cta=d.get("id_cta"),
                                     destino=d["email"], asunto=asunto, mensaje=texto,
                                     tipo=plantilla["id"], id_usuario=id_usuario, estado="EXITOSO",
                                     envio_masivo_id=id_envio)
                if d.get("id_cta"):
                    registrar_contacto_mail(db, d["id_cta"], id_usuario, d["email"], asunto)
            else:
                job.errores += 1
                registrar_envio_mail(db, matricula=d["matricula"], id_cta=d.get("id_cta"),
                                     destino=d["email"], asunto=asunto, mensaje=texto,
                                     tipo=plantilla["id"], id_usuario=id_usuario,
                                     estado=f"ERROR: {resultado['detalle']}", envio_masivo_id=id_envio)
            db.commit()

            # Delays anti-bloqueo (solo si queda cola)
            if idx < len(lote) - 1:
                time.sleep(mail_settings.mail_delay_mensajes)
                if (idx + 1) % mail_settings.mail_tam_lote == 0:
                    time.sleep(mail_settings.mail_delay_lote)
                elif (idx + 1) % 10 == 0:
                    time.sleep(random.randint(2, 6))

        job.estado = "completado"
        job.finalizado_at = datetime.now()
        db.commit()
    except Exception as e:
        db.rollback()
        try:
            job = db.query(MailEnvioMasivo).filter(MailEnvioMasivo.id_envio == id_envio).first()
            if job:
                job.estado = "error"
                job.finalizado_at = datetime.now()
                db.commit()
        except Exception:
            pass
        print(f"[MAIL MASIVO ERROR] job {id_envio}: {e}")
    finally:
        db.close()
