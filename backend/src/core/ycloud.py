import httpx
from pydantic_settings import BaseSettings


class YCloudSettings(BaseSettings):
    ycloud_api_key: str = ""
    ycloud_from: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


ycloud_settings = YCloudSettings()


def enviar_texto(to: str, texto: str) -> dict:
    """
    Envía un mensaje de texto a través de YCloud.
    Si la clave API es vacía o "CHANGEME", simula el envío sin hacer request de red.
    Retorna {"ycloud_id": str|None, "estado": str}
    """
    api_key = ycloud_settings.ycloud_api_key
    ycloud_from = ycloud_settings.ycloud_from

    # Si la clave es vacía o placeholder, simular
    if not api_key or api_key == "CHANGEME":
        print(f"[YCLOUD SIMULADO] Enviando a {to}: {texto}")
        return {"ycloud_id": None, "estado": "simulado"}

    try:
        url = "https://api.ycloud.com/v2/whatsapp/messages"
        headers = {"X-API-Key": api_key}
        payload = {
            "from": ycloud_from,
            "to": to,
            "type": "text",
            "text": {"body": texto},
        }

        response = httpx.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        ycloud_id = data.get("id")
        return {"ycloud_id": ycloud_id, "estado": "enviado"}
    except Exception as e:
        print(f"[YCLOUD ERROR] Fallo enviando a {to}: {e}")
        return {"ycloud_id": None, "estado": "fallido"}
