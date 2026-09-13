"""Utilidades para normalizar montos guardados como texto (VARCHAR).
La deuda puede venir en formato es-AR ('1.278.142,46'), decimal con punto
o entero. Canonizamos a string con punto decimal (parseable por Decimal/float)."""
from decimal import Decimal, InvalidOperation


def normalizar_deuda(v):
    """Devuelve un string canónico con punto decimal, o None si no es numérico."""
    if v is None:
        return None
    if isinstance(v, (int, float, Decimal)):
        return str(v)
    s = str(v).strip()
    if not s:
        return None
    if "," in s:  # es-AR: '.' son separadores de miles y ',' es el decimal
        s = s.replace(".", "").replace(",", ".")
    try:
        Decimal(s)
        return s
    except (InvalidOperation, ValueError):
        return None


def deuda_float(v) -> float:
    """Convierte a float tolerando formato es-AR; 0.0 si no es numérico."""
    s = normalizar_deuda(v)
    if s is None:
        return 0.0
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


# --- Números a letras (para importes de recibos) ---

_UNIDADES = [
    "", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "diecisiete",
    "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidos", "veintitres",
    "veinticuatro", "veinticinco", "veintiseis", "veintisiete", "veintiocho", "veintinueve",
]
_DECENAS = ["", "", "", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
_CENTENAS = [
    "", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos",
    "seiscientos", "setecientos", "ochocientos", "novecientos",
]


def _menor_cien(n: int) -> str:
    if n < 30:
        return _UNIDADES[n]
    d, u = divmod(n, 10)
    return _DECENAS[d] if u == 0 else f"{_DECENAS[d]} y {_UNIDADES[u]}"


def _menor_mil(n: int) -> str:
    if n == 100:
        return "cien"
    c, resto = divmod(n, 100)
    partes = []
    if c:
        partes.append(_CENTENAS[c])
    if resto:
        partes.append(_menor_cien(resto))
    return " ".join(partes)


def _grupo(n: int, singular: str, plural: str) -> str:
    if n == 0:
        return ""
    if n == 1:
        return singular
    return f"{_menor_mil(n)} {plural}"


def entero_a_letras(n: int) -> str:
    """Entero no negativo a palabras. Soporta hasta miles de millones."""
    if n == 0:
        return "cero"
    millones, resto = divmod(n, 1_000_000)
    miles, unidades = divmod(resto, 1000)
    partes = []
    if millones:
        partes.append(_grupo(millones, "un millon", "millones"))
    if miles:
        partes.append(_grupo(miles, "mil", "mil"))
    if unidades:
        partes.append(_menor_mil(unidades))
    return " ".join(p for p in partes if p).strip()


def importe_a_letras(importe) -> str:
    """Importe monetario a letras: 'PESOS ... CON XX/100'."""
    valor = Decimal(str(importe or 0))
    entero = int(valor)
    centavos = int(round((valor - entero) * 100))
    return f"PESOS {entero_a_letras(entero)} CON {centavos:02d}/100".upper()
