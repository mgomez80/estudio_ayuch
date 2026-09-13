"""Cliente HTTP al Hermes Agent (self-hosted, API OpenAI-compatible).
Sin HERMES_API_URL opera en modo simulado (desarrollo sin el VPS)."""
import json

import httpx
from pydantic_settings import BaseSettings


class HermesSettings(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"

    hermes_api_url: str = ""
    hermes_api_key: str = ""
    hermes_model: str = "hermes3"
    hermes_timeout: int = 30


hermes_settings = HermesSettings()


def chat(messages: list[dict], tools: list[dict] | None = None) -> dict:
    """Un turno contra Hermes. Devuelve el message del assistant (content y/o tool_calls)."""
    url = hermes_settings.hermes_api_url
    if not url:
        return {"role": "assistant", "tool_calls": None, "simulado": True,
                "content": "[SIMULADO] Hermes no está configurado (HERMES_API_URL). "
                           "Respuesta de prueba del gestor."}
    payload = {"model": hermes_settings.hermes_model, "messages": messages, "stream": False}
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    headers = {"Authorization": f"Bearer {hermes_settings.hermes_api_key}"} if hermes_settings.hermes_api_key else None

    max_intentos = 2  # NVIDIA/Nemotron tiene latencia variable; 1 reintento ante timeout puntual
    ultimo_error = None
    for intento in range(1, max_intentos + 1):
        try:
            resp = httpx.post(f"{url.rstrip('/')}/v1/chat/completions",
                              json=payload, headers=headers, timeout=hermes_settings.hermes_timeout)
            resp.raise_for_status()
            msg = resp.json()["choices"][0]["message"]
            return {"role": "assistant", "content": msg.get("content"),
                    "tool_calls": msg.get("tool_calls")}
        except httpx.TimeoutException as e:
            ultimo_error = e
            continue  # reintentar; no tiene sentido reintentar otros HTTPError (4xx/5xx no transitorios)
        except (httpx.HTTPError, KeyError, IndexError, json.JSONDecodeError) as e:
            return {"role": "assistant", "tool_calls": None, "error": True,
                    "content": f"No pude consultar al gestor IA: {e}"}
    return {"role": "assistant", "tool_calls": None, "error": True,
            "content": f"No pude consultar al gestor IA: {ultimo_error}"}
