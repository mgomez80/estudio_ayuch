USE db_estudio_lg;

-- Columna requerida para que /whatsapp/webhook/status pueda matchear el
-- status async de YCloud (delivered/failed) contra el log de envíos y
-- corregir el Reporte de Envíos cuando un EXITOSO inicial termina rechazado.

SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'registro_envios_whatsapp' AND column_name = 'ycloud_id'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE registro_envios_whatsapp ADD COLUMN ycloud_id VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @idx_existe = (
  SELECT COUNT(*) FROM information_schema.statistics
  WHERE table_schema = DATABASE() AND table_name = 'registro_envios_whatsapp' AND index_name = 'idx_registro_ycloud_id'
);
SET @ddl = IF(@idx_existe = 0, 'ALTER TABLE registro_envios_whatsapp ADD INDEX idx_registro_ycloud_id (ycloud_id)', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
