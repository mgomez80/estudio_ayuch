-- ============================================================
-- MÓDULOS, PERFILES Y PERMISOS
-- Base del sistema de autorización granular para Configuración
-- ============================================================
SET NAMES utf8mb4;

-- ---------- db_estudio_ayuch: Tablas de catálogo (módulos, perfiles, permisos) ----------
USE db_estudio_ayuch;

CREATE TABLE IF NOT EXISTS `modulos` (
  `id_modulo` int NOT NULL AUTO_INCREMENT,
  `clave` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `desc_modulo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_modulo`),
  UNIQUE KEY `clave` (`clave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `perfiles` (
  `id_perfil` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `activo` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id_perfil`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `perfil_permisos` (
  `perfiles_id_perfil` int NOT NULL,
  `modulos_id_modulo` int NOT NULL,
  `ver` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `alta` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `baja` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `modificar` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`perfiles_id_perfil`,`modulos_id_modulo`),
  KEY `perfil_permisos_FKIndex1` (`modulos_id_modulo`),
  CONSTRAINT `perfil_permisos_fk_modulos` FOREIGN KEY (`modulos_id_modulo`) REFERENCES `modulos` (`id_modulo`),
  CONSTRAINT `perfil_permisos_fk_perfiles` FOREIGN KEY (`perfiles_id_perfil`) REFERENCES `perfiles` (`id_perfil`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Datos seed: Módulos (INSERT IGNORE: `clave` es UNIQUE, no duplica si se re-corre)
INSERT IGNORE INTO modulos (clave, desc_modulo) VALUES
('cuentas', 'Gestión de Cuentas'),
('contactos', 'Registro de Contactos'),
('cobros', 'Gestión de Cobros'),
('agenda', 'Agenda'),
('judicial', 'Módulo Judicial'),
('whatsapp', 'Integración WhatsApp'),
('configuracion', 'Configuración del Sistema');

-- Datos seed: Perfil Administrador (solo si no existe ya)
INSERT INTO perfiles (nombre, activo)
SELECT 'Administrador', 'S' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM perfiles WHERE nombre = 'Administrador');

-- Datos seed: Permisos para Administrador (acceso total a todos los módulos)
-- INSERT IGNORE: PK compuesta (perfil, modulo) no duplica si se re-corre
INSERT IGNORE INTO perfil_permisos (perfiles_id_perfil, modulos_id_modulo, ver, alta, baja, modificar)
SELECT p.id_perfil, m.id_modulo, 'S', 'S', 'S', 'S'
FROM perfiles p, modulos m
WHERE p.nombre = 'Administrador';

-- ---------- db_estudio_ayuch_auth: Agregar relación con perfiles ----------
USE db_estudio_ayuch_auth;

-- MySQL no soporta ALTER TABLE ... ADD COLUMN IF NOT EXISTS (a diferencia de MariaDB),
-- así que el guard de idempotencia se arma a mano con SQL dinámico.
SET @col_existe = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE() AND table_name = 'usuarios' AND column_name = 'perfiles_id_perfil'
);
SET @ddl = IF(@col_existe = 0, 'ALTER TABLE usuarios ADD COLUMN perfiles_id_perfil INT NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
