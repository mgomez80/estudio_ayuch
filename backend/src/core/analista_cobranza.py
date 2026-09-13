"""Lógica pura de análisis de cobranza extrajudicial: score de prioridad, plan de
pago sugerido, compliance de horario de contacto y próxima acción recomendada.
Sin acceso a DB — las señales se calculan en el router y se pasan como dict."""
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

# Feriados nacionales AR 2026 (fijos + trasladables/móviles conocidos al momento de
# escribir esto). Lista estática: actualizar a mano cada año contra el decreto oficial.
FERIADOS_AR: set[date] = {
    date(2026, 1, 1),    # Año Nuevo
    date(2026, 2, 16),   # Carnaval
    date(2026, 2, 17),   # Carnaval
    date(2026, 3, 24),   # Día Nacional de la Memoria
    date(2026, 4, 2),    # Día del Veterano y de los Caídos en Malvinas
    date(2026, 4, 3),    # Viernes Santo
    date(2026, 5, 1),    # Día del Trabajador
    date(2026, 5, 25),   # Revolución de Mayo
    date(2026, 6, 17),   # Paso a la Inmortalidad del Gral. Güemes
    date(2026, 6, 20),   # Día de la Bandera
    date(2026, 7, 9),    # Día de la Independencia
    date(2026, 8, 17),   # Paso a la Inmortalidad del Gral. San Martín
    date(2026, 10, 12),  # Día del Respeto a la Diversidad Cultural
    date(2026, 11, 20),  # Día de la Soberanía Nacional
    date(2026, 12, 8),   # Inmaculada Concepción de María
    date(2026, 12, 25),  # Navidad
}


def calcular_score(señales: dict) -> int:
    """Score 0-100. Pesos: deuda relativa 35, antigüedad 20, judicial 15,
    gestiones sin resultado 10, promesa incumplida 10, convenio caído 10."""
    score = señales["deuda_ratio"] * 35
    score += min(señales["antiguedad_dias"] / 365, 1) * 20
    score += 15 if señales["judicial_activa"] else 0
    score += min(señales["gestiones_sin_resultado"], 3) / 3 * 10
    score += 10 if señales["promesa_incumplida"] else 0
    score += 10 if señales["convenio_caido"] else 0
    return min(100, round(score))


def nivel(score: int) -> str:
    if score >= 70:
        return "ALTA"
    if score >= 40:
        return "MEDIA"
    return "BAJA"


def sugerir_plan(deuda: float) -> dict:
    """Plan de pago sugerido: 3 cuotas si deuda<=100k, 6 si <=500k, 12 si más.
    Anticipo sugerido 20%, redondeo ROUND_HALF_UP (igual que convenios_abm._calcular_plan)."""
    if deuda <= 100_000:
        cant_cuotas = 3
    elif deuda <= 500_000:
        cant_cuotas = 6
    else:
        cant_cuotas = 12

    d = Decimal(str(deuda))
    anticipo = (d * Decimal("0.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    saldo = d - anticipo
    importe_cuota = (saldo / cant_cuotas).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "cant_cuotas": cant_cuotas,
        "anticipo_sugerido": float(anticipo),
        "importe_cuota": float(importe_cuota),
    }


def horario_permitido(ahora: datetime) -> dict:
    """Compliance de horario/día de contacto: L-V 8-20hs, no feriados. No es
    bloqueante en los endpoints que lo usan, solo informativo."""
    if ahora.weekday() >= 5:
        return {"horario_ok": False, "motivo": "Fin de semana"}
    if ahora.date() in FERIADOS_AR:
        return {"horario_ok": False, "motivo": "Feriado"}
    if not (8 <= ahora.hour < 20):
        return {"horario_ok": False, "motivo": "Fuera de horario permitido (8-20hs)"}
    return {"horario_ok": True, "motivo": None}


def proxima_accion(señales: dict) -> str:
    """Primera regla que matchea, en orden de prioridad."""
    if señales["judicial_activa"]:
        return "Derivar a legal antes de contactar."
    if señales["promesa_incumplida"] and señales["gestiones_sin_resultado"] >= 3:
        return "Tono urgente, ofrecer plan de pago como última instancia."
    if señales["convenio_caido"]:
        return "Contactar para regularizar convenio caído, evaluar refinanciación."
    if señales["gestiones_sin_resultado"] == 0:
        return "Primer contacto, tono cordial."
    return "Recordatorio de deuda, tono profesional."
