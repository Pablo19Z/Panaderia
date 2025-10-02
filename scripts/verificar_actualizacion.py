import sqlite3
import os

def verificar_precios():
    """Verifica que los precios estén en pesos colombianos"""
    
    db_path = 'panaderia.db'
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando precios actuales en la base de datos:")
        print("=" * 60)
        
        cursor.execute('''
            SELECT id, nombre, precio, stock 
            FROM productos 
            ORDER BY id
        ''')
        
        productos = cursor.fetchall()
        
        for producto_id, nombre, precio, stock in productos:
            # Formatear precio en pesos colombianos
            precio_formateado = f"${precio:,.0f}"
            print(f"{producto_id}. {nombre:<25} {precio_formateado:>10} (Stock: {stock})")
        
        print("=" * 60)
        
        # Verificar si los precios están en rango de pesos colombianos
        precios_correctos = all(precio >= 1000 for _, _, precio, _ in productos if precio > 100)
        
        if precios_correctos:
            print("✅ Los precios están correctamente configurados en pesos colombianos")
        else:
            print("⚠️  Algunos precios parecen estar aún en dólares")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al verificar precios: {e}")

if __name__ == "__main__":
    verificar_precios()
