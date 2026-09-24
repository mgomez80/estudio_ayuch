-- ============================================================
-- CONCEPTOS DE COBRO (CAPITAL / HONORARIOS)
-- El ABM de Cobros solo admite estos dos conceptos (ver
-- backend/src/routers/cobros_abm.py). Requieren un rubro padre porque
-- conceptos.rubros_id_rubro es NOT NULL.
-- Idempotente: se puede correr las veces que haga falta.
-- ============================================================
SET NAMES utf8mb4;
USE db_estudio_ayuch;

INSERT INTO rubros (desc_rubro, activo)
SELECT 'Cobros', 'S' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM rubros WHERE desc_rubro = 'Cobros');

INSERT INTO conceptos (rubros_id_rubro, desc_concepto, activo)
SELECT r.id_rubro, c.nombre, 'S'
FROM rubros r
CROSS JOIN (SELECT 'CAPITAL' AS nombre UNION ALL SELECT 'HONORARIOS') c
WHERE r.desc_rubro = 'Cobros'
  AND NOT EXISTS (
    SELECT 1 FROM conceptos ex WHERE ex.desc_concepto = c.nombre
  );
