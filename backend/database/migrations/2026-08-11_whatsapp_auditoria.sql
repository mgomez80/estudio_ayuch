USE db_estudio_lg;

-- Agregar columnas de auditoría y metadata a wa_mensajes
-- MySQL no soporta ADD COLUMN IF NOT EXISTS, así que se usa SQL dinámico con information_schema

-- eliminado
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'eliminado'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN eliminado TINYINT NOT NULL DEFAULT 0', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- editado
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'editado'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN editado TINYINT NOT NULL DEFAULT 0', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- editado_en
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'editado_en'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN editado_en DATETIME NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- leido_at
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'leido_at'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN leido_at DATETIME NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- leido_por
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'leido_por'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN leido_por INT NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- media_id
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'media_id'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN media_id VARCHAR(255) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- archivo_nombre
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'archivo_nombre'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN archivo_nombre VARCHAR(200) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- media_mime
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'media_mime'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN media_mime VARCHAR(100) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- texto_original
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'wa_mensajes' AND column_name = 'texto_original'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE wa_mensajes ADD COLUMN texto_original TEXT NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Crear tabla whatsapp_autoreply_control
CREATE TABLE IF NOT EXISTS whatsapp_autoreply_control (
  telefono VARCHAR(30) NOT NULL PRIMARY KEY,
  ultimo_envio DATETIME NULL,
  veces INT NOT NULL DEFAULT 1
);
