import io

import pandas as pd
from fastapi.responses import StreamingResponse


def to_excel_response(rows, columns, filename):
    """
    rows: lista de dicts.
    columns: lista de (clave, encabezado) — define orden y nombres de columna.
    filename: nombre del archivo .xlsx a descargar.
    """
    keys = [c[0] for c in columns]
    headers = [c[1] for c in columns]
    data = [[r.get(k) for k in keys] for r in rows]
    df = pd.DataFrame(data, columns=headers)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Informe")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
