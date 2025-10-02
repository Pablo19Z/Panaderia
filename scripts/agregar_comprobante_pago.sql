-- Script para agregar el campo comprobante_pago a la tabla pedidos
-- Agregando campo para almacenar comprobantes de pago

ALTER TABLE pedidos ADD COLUMN comprobante_pago TEXT;

-- Crear índice para búsquedas por método de pago
CREATE INDEX IF NOT EXISTS idx_pedidos_metodo_pago ON pedidos(metodo_pago);

-- Crear índice para búsquedas por comprobante
CREATE INDEX IF NOT EXISTS idx_pedidos_comprobante ON pedidos(comprobante_pago);
