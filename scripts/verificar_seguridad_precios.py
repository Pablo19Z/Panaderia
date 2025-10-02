"""
Script para verificar que los cambios de precios no afectan las ventas históricas.
Este script demuestra que el sistema usa "price snapshotting" - captura el precio
al momento de la venta y lo guarda permanentemente en detalle_pedidos.
"""

import sqlite3
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.producto import Producto
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

def verificar_seguridad_precios():
    """Verifica que los cambios de precios no afecten ventas históricas"""
    
    print("=" * 70)
    print("VERIFICACIÓN DE SEGURIDAD DE PRECIOS")
    print("=" * 70)
    print()
    
    # 1. Obtener un producto de ejemplo
    productos = Producto.get_all(limit=1)
    if not productos:
        print("❌ No hay productos en la base de datos")
        return False
    
    producto = productos[0]
    precio_original = producto.precio
    
    print(f"📦 Producto seleccionado: {producto.nombre}")
    print(f"💰 Precio actual: ${precio_original:,.2f} COP")
    print()
    
    # 2. Verificar ventas existentes con este producto
    conn = sqlite3.connect('panaderia.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT dp.id, dp.pedido_id, dp.cantidad, dp.precio_unitario, p.fecha_pedido
        FROM detalle_pedidos dp
        JOIN pedidos p ON dp.pedido_id = p.id
        WHERE dp.producto_id = ?
        ORDER BY p.fecha_pedido DESC
        LIMIT 5
    ''', (producto.id,))
    
    ventas_historicas = cursor.fetchall()
    
    if ventas_historicas:
        print("📊 VENTAS HISTÓRICAS ENCONTRADAS:")
        print("-" * 70)
        for venta in ventas_historicas:
            detalle_id, pedido_id, cantidad, precio_guardado, fecha = venta
            print(f"  Pedido #{pedido_id} | Fecha: {fecha}")
            print(f"  Cantidad: {cantidad} | Precio guardado: ${precio_guardado:,.2f} COP")
            print()
    else:
        print("ℹ️  No hay ventas históricas para este producto")
        print()
    
    # 3. Simular cambio de precio
    nuevo_precio = precio_original * 1.5  # Aumentar 50%
    print(f"🔄 SIMULANDO CAMBIO DE PRECIO:")
    print(f"   Precio anterior: ${precio_original:,.2f} COP")
    print(f"   Precio nuevo:    ${nuevo_precio:,.2f} COP")
    print()
    
    # Actualizar precio del producto
    producto.update({'precio': nuevo_precio})
    
    # 4. Verificar que las ventas históricas NO cambiaron
    cursor.execute('''
        SELECT dp.id, dp.pedido_id, dp.cantidad, dp.precio_unitario, p.fecha_pedido
        FROM detalle_pedidos dp
        JOIN pedidos p ON dp.pedido_id = p.id
        WHERE dp.producto_id = ?
        ORDER BY p.fecha_pedido DESC
        LIMIT 5
    ''', (producto.id,))
    
    ventas_despues = cursor.fetchall()
    
    print("✅ VERIFICACIÓN DE INTEGRIDAD:")
    print("-" * 70)
    
    if ventas_historicas:
        todo_correcto = True
        for i, (venta_antes, venta_despues) in enumerate(zip(ventas_historicas, ventas_despues)):
            precio_antes = venta_antes[3]
            precio_despues = venta_despues[3]
            
            if precio_antes == precio_despues:
                print(f"  ✓ Pedido #{venta_antes[1]}: Precio histórico preservado (${precio_antes:,.2f})")
            else:
                print(f"  ✗ Pedido #{venta_antes[1]}: ¡PRECIO CAMBIÓ! ${precio_antes:,.2f} → ${precio_despues:,.2f}")
                todo_correcto = False
        
        print()
        if todo_correcto:
            print("🎉 ¡PERFECTO! Todas las ventas históricas mantienen sus precios originales")
        else:
            print("⚠️  ADVERTENCIA: Algunos precios históricos cambiaron")
    else:
        print("  ℹ️  No hay ventas históricas para verificar")
    
    print()
    
    # 5. Verificar el precio actual del producto
    producto_actualizado = Producto.find_by_id(producto.id)
    print(f"📦 Precio actual del producto en catálogo: ${producto_actualizado.precio:,.2f} COP")
    print()
    
    # 6. Restaurar precio original
    producto.update({'precio': precio_original})
    print(f"🔄 Precio restaurado a: ${precio_original:,.2f} COP")
    print()
    
    # 7. Explicación del sistema
    print("=" * 70)
    print("CÓMO FUNCIONA EL SISTEMA DE PRECIOS")
    print("=" * 70)
    print("""
1. PRECIO EN CATÁLOGO (tabla 'productos'):
   - Este es el precio actual que ven los clientes
   - Puedes cambiarlo cuando quieras
   - Solo afecta a NUEVAS ventas

2. PRECIO EN VENTAS (tabla 'detalle_pedidos'):
   - Cuando se realiza una venta, el precio actual se COPIA a 'precio_unitario'
   - Este precio queda CONGELADO permanentemente
   - Nunca cambia, incluso si cambias el precio del producto

3. BENEFICIOS:
   ✓ Puedes cambiar precios sin miedo
   ✓ Las ventas pasadas mantienen sus precios originales
   ✓ Los PDFs y reportes siempre muestran el precio correcto
   ✓ Auditoría completa del historial de precios

4. SEGURIDAD:
   ✓ No hay referencias dinámicas a precios actuales
   ✓ Cada venta es un registro histórico inmutable
   ✓ Los cambios de precio no afectan cálculos pasados
""")
    
    conn.close()
    return True

if __name__ == '__main__':
    try:
        verificar_seguridad_precios()
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
