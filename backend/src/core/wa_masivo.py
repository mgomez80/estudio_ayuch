import random
import time
from datetime import datetime

from src.core.auth_database import AuthSessionLocal
from src.core.database import SessionLocal
from src.core.wa_n8n import enviar_plantilla, wa_settings
from src.core.wa_registro import (
    conteo_diario, registrar_contacto_whatsapp, registrar_envio, render_texto,
)
from src.models.usuario import Usuario
from src.models.whatsapp import WaConversacion, WaEnvioMasivo


def recortar_por_limite(destinatarios: list, ya_enviados_hoy: int, maximo: int) -> list:
    restante = max(0, maximo - ya_enviados_hoy)
    return destinatarios[:restante]


def _registrar_conversacion(db, telefono, texto, user_id, id_cta, estado):
    """Refleja el envío en wa_conversaciones (last_msg). El wa_mensajes saliente
    lo graba n8n (fuente única, evita duplicar la fila)."""
    conv = db.query(WaConversacion).filter(WaConversacion.telefono == telefono).first()
    if not conv:
        conv = WaConversacion(telefono=telefono, nombre_contacto=None,
                              cuentas_id_cta=id_cta, no_leidos=0,
                              estado="abierta", creado_at=datetime.now())
        db.add(conv)
        db.flush()
    conv.ultimo_mensaje = texto
    conv.ultimo_mensaje_at = datetime.now()


def procesar_envio_masivo(id_envio: int, destinatarios: list[dict],
                          plantilla: dict, id_usuario: int) -> None:
    """Worker background: itera destinatarios con delays anti-bloqueo y
    reintentos; actualiza el job y el log. Nunca lanza (job queda 'error')."""
    db = SessionLocal()
    try:
        job = db.query(WaEnvioMasivo).filter(WaEnvioMasivo.id_envio == id_envio).first()
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
        gestor = (usuario.nombre_completo or usuario.loguin_usuario) if usuario else "Lino Gonzalez"

        lote = recortar_por_limite(
            destinatarios, conteo_diario(db, id_usuario), wa_settings.wa_max_mensajes_dia
        )
        recortados = len(destinatarios) - len(lote)
        if recortados:
            job.errores += recortados
            for d in destinatarios[len(lote):]:
                registrar_envio(db, matricula=d["matricula"], id_cta=d.get("id_cta"),
                                destino=d["telefono"], mensaje="", tipo=plantilla["id"],
                                id_usuario=id_usuario, estado="DESCARTADO: limite diario",
                                envio_masivo_id=id_envio)
            db.commit()

        for idx, d in enumerate(lote):
            # Cada destinatario se procesa aislado: un fallo (envío o registro)
            # nunca debe abortar el lote entero. Se contabiliza y se sigue.
            try:
                texto = render_texto(plantilla["texto"], d.get("nombre"), d.get("cliente"), gestor)

                resultado = None
                for intento in range(1, wa_settings.wa_max_reintentos + 1):
                    resultado = enviar_plantilla(
                        d["telefono"], d.get("nombre") or "Cliente",
                        d.get("cliente") or "nuestro estudio",
                        texto, plantilla["template_name"], gestor=gestor,
                    )
                    if resultado["ok"]:
                        break
                    if intento < wa_settings.wa_max_reintentos:
                        time.sleep(wa_settings.wa_delay_reintento)

                if resultado["ok"]:
                    # El mensaje ya salió por n8n: contabilizar y commitear el
                    # éxito ANTES del historial, para no perderlo ni frenar el
                    # lote si el registro de historial/contacto falla.
                    job.enviados += 1
                    db.commit()
                    try:
                        registrar_envio(db, matricula=d["matricula"], id_cta=d.get("id_cta"),
                                        destino=d["telefono"], mensaje=texto, tipo=plantilla["id"],
                                        id_usuario=id_usuario, estado="EXITOSO",
                                        envio_masivo_id=id_envio, ycloud_id=resultado.get("ycloud_id"))
                        _registrar_conversacion(db, d["telefono"], texto, id_usuario,
                                                d.get("id_cta"), resultado["estado"])
                        if d.get("id_cta"):
                            registrar_contacto_whatsapp(db, d["id_cta"], id_usuario,
                                                        d["telefono"], texto)
                        db.commit()
                    except Exception as e:
                        db.rollback()
                        print(f"[WA MASIVO] historial fallo {d.get('telefono')}: {e}")
                else:
                    job.errores += 1
                    db.commit()
                    try:
                        registrar_envio(db, matricula=d["matricula"], id_cta=d.get("id_cta"),
                                        destino=d["telefono"], mensaje=texto, tipo=plantilla["id"],
                                        id_usuario=id_usuario,
                                        estado=f"ERROR: {resultado['detalle']}",
                                        envio_masivo_id=id_envio)
                        db.commit()
                    except Exception as e:
                        db.rollback()
                        print(f"[WA MASIVO] log error fallo {d.get('telefono')}: {e}")
            except Exception as e:
                # Fallo inesperado en este destinatario: contarlo y continuar.
                db.rollback()
                try:
                    job.errores += 1
                    db.commit()
                except Exception:
                    db.rollback()
                print(f"[WA MASIVO] destinatario {d.get('telefono')} abortado: {e}")

            # Delays anti-bloqueo (solo si queda cola)
            if idx < len(lote) - 1:
                time.sleep(wa_settings.wa_delay_mensajes)
                if (idx + 1) % wa_settings.wa_tam_lote == 0:
                    time.sleep(wa_settings.wa_delay_lote)
                elif (idx + 1) % 10 == 0:
                    time.sleep(random.randint(5, 15))

        job.estado = "completado"
        job.finalizado_at = datetime.now()
        db.commit()
    except Exception as e:
        db.rollback()
        try:
            job = db.query(WaEnvioMasivo).filter(WaEnvioMasivo.id_envio == id_envio).first()
            if job:
                job.estado = "error"
                job.finalizado_at = datetime.now()
                db.commit()
        except Exception:
            pass
        print(f"[WA MASIVO ERROR] job {id_envio}: {e}")
    finally:
        db.close()
