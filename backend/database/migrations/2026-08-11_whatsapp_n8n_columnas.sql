USE db_estudio_lg;

-- Columnas requeridas por el workflow n8n adaptado (manejo_whatsapp_estudio_lg):
-- error_code / error_msg (Actualizar Estado Mensaje) y eliminado_en (Marcar Eliminado)

-- error_code
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'error_code'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN error_code VARCHAR(50) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- error_msg
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'error_msg'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN error_msg VARCHAR(500) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- eliminado_en
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'eliminado_en'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN eliminado_en DATETIME NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- indice unico en ycloud_id (permite NULL multiples) para que el INSERT IGNORE
-- del webhook inbound funcione como guarda de idempotencia ante reintentos de YCloud
SET @idx_existe = (
  SELECT COUNT(*) FROM information_schema.statistics
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND index_name = 'uq_wa_msg_ycloud_id'
);
SET @ddl = IF(@idx_existe = 0, 'ALTER TABLE wa_mensajes ADD UNIQUE KEY uq_wa_msg_ycloud_id (ycloud_id)', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
