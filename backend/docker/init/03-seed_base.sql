-- ============================================================
-- Datos base de parametrización para estudio_lg. Sin datos de cobrosnor.
-- ============================================================
SET NAMES utf8mb4;

-- ---------- db_estudio_ayuch_auth ----------
USE db_estudio_ayuch_auth;

INSERT INTO usuarios (id_usuario, loguin_usuario, password_hash, nombre_completo, rol, activo)
VALUES (1, 'admin', '$2b$12$eRrJ7zl7hgBNsH7jJhF4guY89bj0Hv2EluyqIPjDU8S3rno.X6EDG', 'Administrador Estudio LG', 'admin', 1);
-- Password de prueba: admin123

-- ---------- db_estudio_ayuch ----------
USE db_estudio_ayuch;

INSERT INTO clientes (id_cliente, cuenta_cliente, desc_cliente, activo) VALUES
(1, 1, 'Estudio LG', 'S');

INSERT INTO subclientes (id_subcli, clientes_id_cliente, clientes_cuenta_cliente, nombre_subcli, activo_subcli) VALUES
(1, 1, 1, 'Cartera General', 'S');

INSERT INTO estados (id_estado, desc_estado, tipo_estado, activo) VALUES
(1, 'Gestión Extrajudicial', 'extrajudicial', 'S'),
(2, 'En Convenio', 'extrajudicial', 'S'),
(3, 'Judicial', 'judicial', 'S');

INSERT INTO sub_estados (id_sub_est, estados_id_estado, desc_sub_est, activo) VALUES
(1, 1, 'Sin contacto', 'S'),
(2, 1, 'Contactado - Promesa de pago', 'S'),
(3, 2, 'Convenio al día', 'S'),
(4, 1, 'EN GESTION', 'S');

INSERT INTO acciones (id_accion, desc_accion, activa) VALUES
(1, 'Llamada telefónica', 'S'),
(2, 'WhatsApp', 'S'),
(3, 'Visita domiciliaria', 'S');

INSERT INTO resultados (id_resultado, desc_resultado, positivo, activo) VALUES
(1, 'Contacto exitoso - Compromiso de pago', 'S', 'S'),
(2, 'No contesta', 'N', 'S'),
(3, 'Número equivocado', 'N', 'S');
