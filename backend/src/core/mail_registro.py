from datetime import date, datetime

from src.models.catalogos import Accion, Resultado
from src.models.contactos import Contacto
from src.models.mail import RegistroEnvioMail


def conteo_diario_mail(db, id_usuario: int) -> int:
    """Mails registrados hoy por el usuario (para el límite diario)."""
    from sqlalchemy import func
    hoy = date.today()
    return (
        db.query(func.count(RegistroEnvioMail.id))
        .filter(
            func.date(RegistroEnvioMail.fecha_envio) == hoy,
            RegistroEnvioMail.id_usuario == id_usuario,
        )
        .scalar()
    ) or 0


def registrar_envio_mail(db, *, matricula, id_cta, destino, asunto, mensaje, tipo,
                         id_usuario, estado, envio_masivo_id=None) -> None:
    db.add(RegistroEnvioMail(
        matricula=matricula, cuentas_id_cta=id_cta, destino=destino, asunto=asunto,
        mensaje=mensaje, tipo=tipo, id_usuario=id_usuario, estado=estado,
        fecha_envio=datetime.now(), envio_masivo_id=envio_masivo_id,
    ))


def registrar_contacto_mail(db, id_cta: int, id_usuario: int,
                            destino: str, asunto: str) -> None:
    """Registra la gestión en contactos: acción MAIL / resultado ENVIADO buscados
    por descripción, fallback ids 8/8 (mismo patrón que registrar_contacto_whatsapp)."""
    accion = db.query(Accion).filter(Accion.desc_accion == "MAIL", Accion.activa == "S").first()
    resultado = db.query(Resultado).filter(Resultado.desc_resultado == "ENVIADO", Resultado.activo == "S").first()
    ahora = datetime.now()
    db.add(Contacto(
        usuarios_id_usuario=id_usuario,
        cuentas_id_cta=id_cta,
        resultados_id_resultado=resultado.id_resultado if resultado else 8,
        acciones_id_accion=accion.id_accion if accion else 8,
        fecha_contacto=ahora.date(),
        hora_contacto=ahora.strftime("%H:%M:%S"),
        nota_contacto=f"Mail a {destino} ({asunto}): enviado".encode(),
        activo="S",
    ))
