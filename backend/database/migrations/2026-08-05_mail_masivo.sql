-- UP: envío masivo de mail (job + log), mismo patrón que wa_envios_masivos / registro_envios_whatsapp
CREATE TABLE IF NOT EXISTS mail_envios_masivos (
  id_envio INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  tipo_mensaje VARCHAR(50) NOT NULL,
  origen VARCHAR(10) NOT NULL,
  total INT NOT NULL DEFAULT 0,
  enviados INT NOT NULL DEFAULT 0,
  errores INT NOT NULL DEFAULT 0,
  descartados_sin_cliente INT NOT NULL DEFAULT 0,
  descartados_duplicados INT NOT NULL DEFAULT 0,
  estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
  creado_at DATETIME NOT NULL,
  finalizado_at DATETIME NULL
);

-- registro_envios_mail ya existía en algunos entornos como tabla legacy chica
-- (matricula, destino, mensaje, tipo, id_usuario, estado, fecha_envio). Se crea
-- si falta, y se completa con las columnas que necesita el job masivo nuevo.
CREATE TABLE IF NOT EXISTS registro_envios_mail (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  matricula VARCHAR(50) NULL,
  destino VARCHAR(255) NULL,
  mensaje TEXT NULL,
  tipo VARCHAR(50) NULL,
  id_usuario INT NULL,
  estado VARCHAR(255) NULL,
  fecha_envio DATETIME NULL
);

ALTER TABLE registro_envios_mail
  ADD COLUMN IF NOT EXISTS cuentas_id_cta INT NULL AFTER matricula,
  ADD COLUMN IF NOT EXISTS asunto VARCHAR(250) NULL AFTER destino,
  ADD COLUMN IF NOT EXISTS envio_masivo_id INT NULL;

-- Índices por separado: ADD INDEX no soporta IF NOT EXISTS en MySQL 8;
-- si la migración ya corrió, ignorar el error 1061 (duplicate key name).
ALTER TABLE registro_envios_mail ADD INDEX idx_registro_envios_mail_usuario (id_usuario);
ALTER TABLE registro_envios_mail ADD INDEX idx_registro_envios_mail_fecha (fecha_envio);

-- DOWN
-- ALTER TABLE registro_envios_mail DROP INDEX idx_registro_envios_mail_fecha, DROP INDEX idx_registro_envios_mail_usuario, DROP COLUMN envio_masivo_id, DROP COLUMN asunto, DROP COLUMN cuentas_id_cta;
-- DROP TABLE mail_envios_masivos;
