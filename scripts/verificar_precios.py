import sqlite3
import sys
import os

def verificar_precios():
    """Verifica los precios actuales en la base de datos"""
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('panaderia.db')
        cursor = conn.cursor()
        
        print("=== PRECIOS ACTUALES EN LA BASE DE DATOS ===")
        print()
        
        # Obtener todos los productos con sus precios
        cursor.execute("""
            SELECT p.nombre, p.precio, p.stock, c.nombre as categoria
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = 1
            ORDER BY p.nombre
        """)
        
        productos = cursor.fetchall()
        
        if not productos:
            print("❌ No se encontraron productos en la base de datos")
            return False
        
        total_productos = len(productos)
        
        for nombre, precio, stock, categoria in productos:
            # Formatear precio con separadores de miles
            precio_formateado = f"${precio:,.0f}".replace(",", ".")
            print(f"📦 {nombre}")
            print(f"   💰 Precio: {precio_formateado}")
            print(f"   📊 Stock: {stock} disponibles")
            print(f"   🏷️  Categoría: {categoria}")
            print()
        
        print(f"✅ Total de productos activos: {total_productos}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar precios: {e}")
        return False

if __name__ == "__main__":
    verificar_precios()
