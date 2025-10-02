import sqlite3
import os

def actualizar_precios_pesos_colombianos():
    """Actualiza los precios existentes en la base de datos a pesos colombianos"""
    
    # Conectar a la base de datos
    db_path = 'panaderia.db'
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Actualizando precios a pesos colombianos...")
        
        # Mapeo de precios: ID del producto -> nuevo precio en pesos colombianos
        nuevos_precios = {
            1: 2500.00,   # Pan Francés: $2.50 -> $2.500
            2: 3500.00,   # Croissant: $3.00 -> $3.500  
            3: 32000.00,  # Torta de Chocolate: $25.00 -> $32.000
            4: 1500.00,   # Galletas de Avena: $1.50 -> $1.500
            5: 2800.00,   # Café Americano: $2.00 -> $2.800
            6: 8500.00    # Sandwich de Jamón: $5.50 -> $8.500
        }
        
        # Actualizar cada producto
        for producto_id, nuevo_precio in nuevos_precios.items():
            cursor.execute('''
                UPDATE productos 
                SET precio = ? 
                WHERE id = ?
            ''', (nuevo_precio, producto_id))
            
            # Verificar que se actualizó
            cursor.execute('SELECT nombre, precio FROM productos WHERE id = ?', (producto_id,))
            resultado = cursor.fetchone()
            if resultado:
                nombre, precio = resultado
                print(f"✅ {nombre}: ${precio:,.0f}")
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar todos los productos actualizados
        print("\n📋 Verificación final de precios:")
        cursor.execute('SELECT id, nombre, precio FROM productos ORDER BY id')
        productos = cursor.fetchall()
        
        for producto_id, nombre, precio in productos:
            print(f"   {producto_id}. {nombre}: ${precio:,.0f}")
        
        conn.close()
        print("\n✅ ¡Precios actualizados exitosamente a pesos colombianos!")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar precios: {e}")
        return False

if __name__ == "__main__":
    actualizar_precios_pesos_colombianos()
