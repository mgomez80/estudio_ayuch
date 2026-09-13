-- El Reporte de Envíos WhatsApp lee la trazabilidad real de entrega desde la base
-- del bot (whatsapp_bot_estudio_lg.mensajes) con la MISMA conexión de la app
-- (ambas bases viven en el mismo servidor MySQL). El usuario de la app necesita
-- permiso de solo lectura sobre esa base.
--
-- Reemplazar <APP_DB_USER> y <APP_DB_HOST> por el usuario/host reales del backend
-- en el VPS (los del .env de producción: DB_USER / host desde el que conecta).
-- Ej. en Docker suele ser '%' o el nombre del contenedor de red.

GRANT SELECT ON `whatsapp_bot_estudio_lg`.* TO '<APP_DB_USER>'@'<APP_DB_HOST>';
FLUSH PRIVILEGES;

-- Verificación:
-- SHOW GRANTS FOR '<APP_DB_USER>'@'<APP_DB_HOST>';
