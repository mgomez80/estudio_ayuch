-- UP: trazabilidad de anulación de cobros (soft-delete)
ALTER TABLE cobros
  ADD COLUMN anulado CHAR(1) NOT NULL DEFAULT 'N' AFTER rendido,
  ADD COLUMN anulado_por INT NULL AFTER anulado,
  ADD COLUMN anulado_ts DATETIME NULL AFTER anulado_por;

-- DOWN
-- ALTER TABLE cobros DROP COLUMN anulado_ts, DROP COLUMN anulado_por, DROP COLUMN anulado;
