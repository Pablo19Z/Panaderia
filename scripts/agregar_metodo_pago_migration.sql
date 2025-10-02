-- Adding metodo_pago column to existing pedidos table
-- Migration script to add metodo_pago column to pedidos table
-- This script is safe to run multiple times

-- Add metodo_pago column if it doesn't exist
ALTER TABLE pedidos ADD COLUMN metodo_pago TEXT DEFAULT 'efectivo';

-- Update existing records to have 'efectivo' as default payment method
UPDATE pedidos SET metodo_pago = 'efectivo' WHERE metodo_pago IS NULL;

-- Verify the migration
SELECT COUNT(*) as total_pedidos, 
       COUNT(metodo_pago) as pedidos_with_payment_method 
FROM pedidos;
