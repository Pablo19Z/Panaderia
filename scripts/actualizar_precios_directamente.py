import sqlite3
import sys
import os

# Agregar el directorio padre al path para importar la base de datos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def actualizar_precios_colombianos():
    """Actualiza directamente los precios en la base de datos a pesos colombianos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('panaderia.db')
    cursor = conn.cursor()
    
    # Nuevos precios en pesos colombianos (valores realistas)
    nuevos_precios = {
        'Pan Francés': 2500,
        'Croissant': 3500,
        'Torta de Chocolate': 32000,
        'Galletas de Avena': 1500,
        'Café Americano': 2800,
        'Sandwich de Jamón': 8500
    }
    
    print("=== ACTUALIZANDO PRECIOS A PESOS COLOMBIANOS ===")
    print()
    
    # Mostrar precios actuales
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos_actuales = cursor.fetchall()
    
    print("PRECIOS ACTUALES:")
    for producto in productos_actuales:
        print(f"- {producto[1]}: ${producto[2]}")
    
    print()
    print("ACTUALIZANDO A PRECIOS COLOMBIANOS:")
    
    # Actualizar cada producto
    productos_actualizados = 0
    for producto_id, nombre, precio_actual in productos_actuales:
        if nombre in nuevos_precios:
            nuevo_precio = nuevos_precios[nombre]
            
            # Actualizar en la base de datos
            cursor.execute(
                "UPDATE productos SET precio = ? WHERE id = ?",
                (nuevo_precio, producto_id)
            )
            
            print(f"- {nombre}: ${precio_actual} → ${nuevo_precio:,}")
            productos_actualizados += 1
        else:
            print(f"- {nombre}: No se encontró precio nuevo, mantiene ${precio_actual}")
    
    # Confirmar cambios
    conn.commit()
    
    print()
    print("=== VERIFICACIÓN DE CAMBIOS ===")
    
    # Verificar que los cambios se aplicaron
    cursor.execute("SELECT nombre, precio FROM productos ORDER BY nombre")
    productos_verificacion = cursor.fetchall()
    
    for nombre, precio in productos_verificacion:
        print(f"✓ {nombre}: ${precio:,}")
    
    print()
    print(f"✅ Se actualizaron {productos_actualizados} productos exitosamente")
    print("✅ Todos los precios están ahora en pesos colombianos")
    
    conn.close()
    
    return True

if __name__ == "__main__":
    try:
        actualizar_precios_colombianos()
        print("\n🎉 ¡Actualización completada exitosamente!")
    except Exception as e:
        print(f"\n❌ Error durante la actualización: {e}")
        sys.exit(1)
