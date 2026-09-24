import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.auth_database import get_auth_db
from src.core.security import get_current_user
from src.core.numeros import normalizar_deuda

router = APIRouter(tags=["Carga masiva"])

# entidad -> (tabla, columnas de datos permitidas, flag)
STAGING = {
    "cuentas": ("carga_masiva_ctas",
        ["matricula", "nombre", "contacto", "monto_deuda", "fecha_deuda",
         "fecha_asignacion", "empleador", "cuenta_cliente", "id_sub_cliente",
         "observacion", "mora"], "cta_actualizada"),
    "telefonos": ("carga_masiva_tel",
        ["matricula", "tipo", "codigo_area", "numero_tel", "observaciones"],
        "tel_actualizado"),
    "direcciones": ("carga_masiva_dir",
        ["matricula", "calle_dir", "nro_dir", "piso_dir", "dpto_dir", "casa_dir",
         "manzana_dir", "barrio_dir", "CP_dir", "localidad_dir", "departamento_dir",
         "provincia_dir", "seccional_dir", "tipo_dir", "observacion_dir"],
        "dir_actualizada"),
    "mails": ("carga_masiva_mail", ["matricula", "mail"], "mail_actualizado"),
    "contactos": ("carga_masiva_contactos",
        ["matricula", "accion", "resultado", "fecha_contacto", "hora_contacto", "nota"],
        "contacto_actualizado"),
}


def _decodificar(raw: bytes) -> str:
    # Excel es-AR exporta CSV en ANSI (Windows-1252), no UTF-8. Intentamos UTF-8
    # (con BOM) y si falla caemos a cp1252 para no romper con acentos/Ñ.
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


def _separador(texto: str) -> str:
    # Si la primera línea trae ';' usamos ';' (Excel es-AR); si no, ','.
    primera = next((l for l in texto.splitlines() if l.strip()), "")
    return ";" if ";" in primera else ","


def _leer_csv(raw: bytes):
    texto = _decodificar(raw)
    return list(csv.DictReader(io.StringIO(texto), delimiter=_separador(texto)))


def _leer_filas(raw: bytes):
    """Lee el CSV posicionalmente (por orden de columnas, sin depender del
    nombre del encabezado). Descarta filas totalmente vacías."""
    texto = _decodificar(raw)
    filas = csv.reader(io.StringIO(texto), delimiter=_separador(texto))
    return [row for row in filas if any((c or "").strip() for c in row)]


@router.post("/carga-masiva/{entidad}")
async def carga_masiva(
    entidad: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    if entidad not in STAGING:
        raise HTTPException(status_code=400, detail=f"Entidad inválida: {entidad}")
    tabla, columnas, flag = STAGING[entidad]
    nombres_col = {c.lower() for c in columnas}

    filas = _leer_filas(await file.read())
    if not filas:
        raise HTTPException(status_code=422, detail="CSV vacío o sin filas.")

    # Encabezado opcional: si la primera fila parece cabecera, se descarta.
    # El mapeo es POSICIONAL — el orden de las columnas define el destino, no el nombre.
    # La matrícula (1ª columna) es un DNI/CUIT numérico; si la 1ª celda trae letras,
    # es un encabezado (con cualquier nombre), no un dato.
    primera = [(c or "").strip().lower() for c in filas[0]]
    if primera and (
        any(ch.isalpha() for ch in primera[0])
        or all(c in nombres_col for c in primera if c)
    ):
        filas = filas[1:]

    insertadas = 0
    errores = []
    for i, fila in enumerate(filas, start=1):
        valores = [(c.strip() if c and c.strip() else None) for c in fila]
        datos = {columnas[j]: valores[j] for j in range(min(len(columnas), len(valores)))}
        if not datos.get("matricula"):
            errores.append({"fila": i, "motivo": "matricula vacía"})
            continue
        datos[flag] = "N"
        cols = ", ".join(f"`{c}`" for c in datos)
        params = ", ".join(f":{c.replace(' ', '_')}" for c in datos)
        bind = {c.replace(" ", "_"): v for c, v in datos.items()}
        try:
            db.execute(text(f"INSERT INTO {tabla} ({cols}) VALUES ({params})"), bind)
            insertadas += 1
        except Exception as e:  # noqa: BLE001
            orig = getattr(e, "orig", None)
            errores.append({"fila": i, "motivo": str(orig) if orig else e.__class__.__name__})
    db.commit()
    return {"entidad": entidad, "insertadas": insertadas, "errores": errores}


# ---------------------------------------------------------------------------
# Promoción: del staging (temporal) a las tablas reales, y vaciado del staging.
# ---------------------------------------------------------------------------

# entidad -> (tabla_real, {col_staging: col_real}, {col_real: valor_default})
PROMOCION_SIMPLE = {
    "telefonos": ("telefonos", {
        "matricula": "entidades_matricula_ent", "tipo": "tipo_tel",
        "codigo_area": "codigo_area_tel", "numero_tel": "numero_tel",
        "observaciones": "observaciones_tel",
    }, {"activo_tel": "S"}),
    "direcciones": ("direcciones", {
        "matricula": "entidades_matricula_ent", "calle_dir": "calle_dir",
        "nro_dir": "nro_dir", "piso_dir": "piso_dir", "dpto_dir": "dpto_dir",
        "casa_dir": "casa_dir", "manzana_dir": "manzana_dir", "barrio_dir": "barrio_dir",
        "CP_dir": "CP_dir", "localidad_dir": "localidad_dir",
        "departamento_dir": "departamento_dir", "provincia_dir": "provincia_dir",
        "seccional_dir": "seccional_dir", "tipo_dir": "tipo_dir",
        "observacion_dir": "observacion_dir",
    }, {"activa_dir": "S"}),
    "mails": ("mails", {
        "matricula": "entidades_matricula_ent", "mail": "mail",
    }, {"activo_mail": "S"}),
}


def _parse_fecha(v):
    if not v:
        return None
    v = str(v).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y", "%Y/%m/%d"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def _limpiar(v):
    return v.strip() if isinstance(v, str) and v.strip() else (None if v in (None, "") else v)


def _borrar_fila_staging(db: Session, tabla_stg: str, cols: list[str], row) -> None:
    """Borra del staging la fila recién promovida, por coincidencia exacta de todas sus
    columnas (estas tablas no tienen PK propia). Alcanza con borrar 1 fila (LIMIT 1):
    si hay duplicados exactos son indistinguibles entre sí y da igual cuál se borre."""
    condiciones, params = [], {}
    for c in cols:
        v = row[c] if isinstance(row, dict) else getattr(row, c)
        if v is None:
            condiciones.append(f"`{c}` IS NULL")
        else:
            condiciones.append(f"`{c}` = :w_{c}")
            params[f"w_{c}"] = v
    where = " AND ".join(condiciones)
    db.execute(text(f"DELETE FROM {tabla_stg} WHERE {where} LIMIT 1"), params)


def _contar_restantes(db: Session, tabla_stg: str) -> int:
    return db.execute(text(f"SELECT COUNT(*) FROM {tabla_stg}")).scalar() or 0


def _procesar_simple(db: Session, tabla_stg: str, conf, lote: int) -> dict:
    """Promueve hasta `lote` filas del staging a la tabla real. Cada fila se borra del
    staging apenas se promueve con éxito, así una tanda con errores no bloquea ni repite
    las que ya salieron bien; las filas con error quedan para corregir y reintentar."""
    tabla_real, mapa, defaults = conf
    stg_cols = list(mapa.keys())
    sel = ", ".join(f"`{c}`" for c in stg_cols)
    filas = db.execute(text(f"SELECT {sel} FROM {tabla_stg} LIMIT :lote"), {"lote": lote}).fetchall()

    promovidas, errores = 0, []
    for i, row in enumerate(filas, start=1):
        d = dict(zip(stg_cols, row))
        if not _limpiar(d.get("matricula")):
            errores.append({"fila": i, "motivo": "matricula vacía"})
            continue
        real = {mapa[c]: _limpiar(v) for c, v in d.items()}
        real.update(defaults)
        cols = ", ".join(f"`{c}`" for c in real)
        params = ", ".join(f":{c}" for c in real)
        try:
            db.execute(text(f"INSERT INTO {tabla_real} ({cols}) VALUES ({params})"), real)
            _borrar_fila_staging(db, tabla_stg, stg_cols, d)
            promovidas += 1
        except Exception as e:  # noqa: BLE001
            errores.append({"fila": i, "motivo": str(getattr(e, "orig", e))})

    db.commit()
    restantes = _contar_restantes(db, tabla_stg)
    return {"promovidas": promovidas, "errores": errores, "restantes": restantes, "vaciado": restantes == 0}


def _procesar_cuentas(db: Session, tabla_stg: str, lote: int) -> dict:
    cols = ["matricula", "nombre", "contacto", "monto_deuda", "fecha_deuda",
            "fecha_asignacion", "empleador", "cuenta_cliente", "id_sub_cliente",
            "observacion", "mora"]
    sel = ", ".join(f"`{c}`" for c in cols)
    filas = db.execute(text(f"SELECT {sel} FROM {tabla_stg} LIMIT :lote"), {"lote": lote}).fetchall()

    errores, validas = [], []
    for i, row in enumerate(filas, start=1):
        d = {c: _limpiar(v) for c, v in zip(cols, row)}
        if not d.get("matricula"):
            errores.append({"fila": i, "motivo": "matricula vacía"})
            continue
        sub = str(d.get("id_sub_cliente") or "").strip()
        if not sub.isdigit():
            errores.append({"fila": i, "motivo": "id_sub_cliente vacío o no numérico"})
            continue
        validas.append((i, d, int(sub)))

    campos_cta = ["deudaact_cta", "fechaingreso_cta", "fecha_asignacion_cta",
                  "empleador_cta", "cuenta_cliente", "observacion_cta", "mora"]
    promovidas = 0
    for i, d, sub in validas:
        m = d["matricula"]
        try:
            # Entidad: upsert por matrícula (no pisa con nulos).
            if db.execute(text("SELECT 1 FROM entidades WHERE matricula_ent=:m"), {"m": m}).first():
                db.execute(text(
                    "UPDATE entidades SET razon_social_ent=COALESCE(:n,razon_social_ent), "
                    "contacto_ent=COALESCE(:c,contacto_ent) WHERE matricula_ent=:m"),
                    {"n": d.get("nombre"), "c": d.get("contacto"), "m": m})
            else:
                db.execute(text(
                    "INSERT INTO entidades (matricula_ent,razon_social_ent,contacto_ent,activo_ent) "
                    "VALUES (:m,:n,:c,'S')"),
                    {"m": m, "n": d.get("nombre"), "c": d.get("contacto")})

            valores = {
                "deudaact_cta": normalizar_deuda(d.get("monto_deuda")),
                "fechaingreso_cta": _parse_fecha(d.get("fecha_deuda")),
                "fecha_asignacion_cta": d.get("fecha_asignacion"),
                "empleador_cta": d.get("empleador"),
                "cuenta_cliente": d.get("cuenta_cliente"),
                "observacion_cta": d.get("observacion"),
                "mora": d.get("mora"),
            }
            # Cuenta: upsert por (matrícula + subcliente).
            existe = db.execute(text(
                "SELECT id_cta FROM cuentas WHERE entidades_matricula_ent=:m "
                "AND subclientes_id_subcli=:s"), {"m": m, "s": sub}).first()
            if existe:
                sets = ", ".join(f"`{k}`=COALESCE(:{k},`{k}`)" for k in campos_cta)
                db.execute(text(f"UPDATE cuentas SET {sets} WHERE id_cta=:id"),
                           {**valores, "id": existe[0]})
            else:
                allc = {"entidades_matricula_ent": m, "subclientes_id_subcli": sub,
                        "activa_cta": "S", "judicial": "N", **valores}
                ci = ", ".join(f"`{k}`" for k in allc)
                pi = ", ".join(f":{k}" for k in allc)
                db.execute(text(f"INSERT INTO cuentas ({ci}) VALUES ({pi})"), allc)
            _borrar_fila_staging(db, tabla_stg, cols, d)
            promovidas += 1
        except Exception as e:  # noqa: BLE001
            errores.append({"fila": i, "motivo": str(getattr(e, "orig", e))})

    db.commit()
    restantes = _contar_restantes(db, tabla_stg)
    return {"promovidas": promovidas, "errores": errores, "restantes": restantes, "vaciado": restantes == 0}


@router.post("/carga-masiva/{entidad}/procesar")
async def procesar_carga(
    entidad: str,
    lote: int = Query(200, ge=1, le=2000),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    """Promueve hasta `lote` filas del staging a las tablas reales (en tandas, para no
    agotar el timeout del proxy con cargas grandes). Llamar repetidas veces hasta que
    la respuesta traiga restantes=0."""
    if entidad not in STAGING:
        raise HTTPException(status_code=400, detail=f"Entidad inválida: {entidad}")
    tabla_stg = STAGING[entidad][0]
    if entidad == "cuentas":
        return _procesar_cuentas(db, tabla_stg, lote)
    if entidad in PROMOCION_SIMPLE:
        return _procesar_simple(db, tabla_stg, PROMOCION_SIMPLE[entidad], lote)
    raise HTTPException(status_code=400,
                        detail=f"La promoción de '{entidad}' todavía no está soportada.")


def _matriculas_csv(raw: bytes):
    filas = _leer_csv(raw)
    return [f.get("matricula", "").strip() for f in filas
            if (f.get("matricula") or "").strip()]


@router.post("/cambios-masivos/reasignacion")
async def reasignacion(
    file: UploadFile = File(...),
    ejecutivo: int = Form(...),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    mats = _matriculas_csv(await file.read())
    afectadas, no_encontradas = 0, []
    for m in mats:
        r = db.execute(
            text("UPDATE cuentas SET ejecutivo=:e WHERE entidades_matricula_ent=:m"),
            {"e": ejecutivo, "m": m},
        )
        if r.rowcount:
            afectadas += r.rowcount
        else:
            no_encontradas.append(m)
    db.commit()
    return {"afectadas": afectadas, "no_encontradas": no_encontradas}


@router.post("/cambios-masivos/sub-estado")
async def cambio_sub_estado(
    file: UploadFile = File(...),
    id_sub_est: int = Form(...),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    existe = db.execute(
        text("SELECT 1 FROM sub_estados WHERE id_sub_est=:id"), {"id": id_sub_est}
    ).first()
    if not existe:
        raise HTTPException(status_code=404, detail="Sub-estado inexistente")
    mats = _matriculas_csv(await file.read())
    afectadas, no_encontradas = 0, []
    for m in mats:
        r = db.execute(
            text("UPDATE cuentas SET sub_estados_id_sub_est=:s "
                 "WHERE entidades_matricula_ent=:m"),
            {"s": id_sub_est, "m": m},
        )
        if r.rowcount:
            afectadas += r.rowcount
        else:
            no_encontradas.append(m)
    db.commit()
    return {"afectadas": afectadas, "no_encontradas": no_encontradas}


@router.get("/catalogos/sub_estados")
def listar_sub_estados(
    db: Session = Depends(get_db), _user: dict = Depends(get_current_user)
):
    rows = db.execute(
        text("SELECT id_sub_est, desc_sub_est FROM sub_estados WHERE activo='S' ORDER BY id_sub_est")
    ).all()
    return [{"id_sub_est": r[0], "desc_sub_est": r[1]} for r in rows]


@router.get("/catalogos/ejecutivos")
def listar_ejecutivos(
    auth_db: Session = Depends(get_auth_db), _user: dict = Depends(get_current_user)
):
    # cuentas.ejecutivo es id_usuario; los usuarios viven en la DB de auth.
    rows = auth_db.execute(
        text("SELECT id_usuario, COALESCE(NULLIF(nombre_completo,''), loguin_usuario) "
             "FROM usuarios WHERE activo=1 ORDER BY loguin_usuario")
    ).all()
    return [{"id_usuario": r[0], "nombre": r[1]} for r in rows]
