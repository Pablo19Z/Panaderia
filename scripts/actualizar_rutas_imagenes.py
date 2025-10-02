import sqlite3
import os

def actualizar_rutas_imagenes():
    """Actualiza las rutas de imágenes en la base de datos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('panaderia.db')
    cursor = conn.cursor()
    
    try:
        # Obtener todos los productos
        cursor.execute("SELECT id, nombre FROM productos ORDER BY id")
        productos = cursor.fetchall()
        
        print("Actualizando rutas de imágenes...")
        
        for producto_id, nombre in productos:
            # Generar ruta de imagen usando placeholder con query específico
            nombre_archivo = f"producto_{producto_id:02d}.jpg"
            
            ruta_imagen = f"/placeholder.svg?height=400&width=400"
            
            # Actualizar en la base de datos
            cursor.execute("""
                UPDATE productos 
                SET imagen = ? 
                WHERE id = ?
            """, (ruta_imagen, producto_id))
            
            print(f"✓ Actualizado producto {producto_id}: {nombre} -> placeholder image")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n¡Actualizadas las rutas de {len(productos)} productos!")
        print("Ahora todas las imágenes usarán placeholders específicos para cada producto.")
        
    except Exception as e:
        print(f"Error al actualizar rutas: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    actualizar_rutas_imagenes()
