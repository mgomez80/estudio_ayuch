from datetime import date, datetime

from src.models.catalogos import Accion, Resultado
from src.models.contactos import Contacto
from src.models.whatsapp import RegistroEnvioWhatsapp


def render_texto(texto: str, nombre: str | None, cliente: str | None,
                 gestor: str | None = None) -> str:
    nombre = nombre or "Cliente"
    cliente = cliente or "nuestro estudio"
    gestor = gestor or ""
    return (texto.replace("%NOMBRE%", nombre)
                .replace("%CLIENTE%", cliente)
                .replace("%GESTOR%", gestor))


def conteo_diario(db, id_usuario: int) -> int:
    """Mensajes registrados hoy por el usuario (para el límite diario)."""
    from sqlalchemy import func
    hoy = date.today()
    return (
        db.query(func.count(RegistroEnvioWhatsapp.id))
        .filter(
            func.date(RegistroEnvioWhatsapp.fecha_envio) == hoy,
            RegistroEnvioWhatsapp.id_usuario == id_usuario,
        )
        .scalar()
    ) or 0


def registrar_envio(db, *, matricula, id_cta, destino, mensaje, tipo,
                    id_usuario, estado, envio_masivo_id=None, ycloud_id=None) -> None:
    db.add(RegistroEnvioWhatsapp(
        matricula=matricula, cuentas_id_cta=id_cta, destino=destino,
        mensaje=mensaje, tipo=tipo, id_usuario=id_usuario, estado=estado,
        fecha_envio=datetime.now(), envio_masivo_id=envio_masivo_id,
        ycloud_id=ycloud_id,
    ))


def registrar_contacto_whatsapp(db, id_cta: int, id_usuario: int,
                                destino: str, mensaje: str) -> None:
    """Registra la gestión en contactos como el legacy: acción WHATSAPP /
    resultado ENVIADO buscados por descripción, fallback ids 8/8."""
    accion = db.query(Accion).filter(Accion.desc_accion == "WHATSAPP", Accion.activa == "S").first()
    resultado = db.query(Resultado).filter(Resultado.desc_resultado == "ENVIADO", Resultado.activo == "S").first()
    ahora = datetime.now()
    db.add(Contacto(
        usuarios_id_usuario=id_usuario,
        cuentas_id_cta=id_cta,
        resultados_id_resultado=resultado.id_resultado if resultado else 8,
        acciones_id_accion=accion.id_accion if accion else 8,
        fecha_contacto=ahora.date(),
        hora_contacto=ahora.strftime("%H:%M:%S"),
        nota_contacto=f"WhatsApp a {destino}: {mensaje}".encode(),
        activo="S",
    ))
