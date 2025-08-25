#!/usr/bin/env python3
"""
Script para actualizar las imágenes de productos con rutas reales
"""

import sqlite3
import os

def actualizar_imagenes_reales():
    """Actualiza las rutas de imágenes a rutas reales sin placeholder"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('panaderia.db')
    cursor = conn.cursor()
    
    try:
        # Obtener todos los productos
        cursor.execute("SELECT id, nombre FROM productos ORDER BY id")
        productos = cursor.fetchall()
        
        print("Actualizando a imágenes reales...")
        
        for producto_id, nombre in productos:
            # Generar ruta de imagen real
            nombre_archivo = f"producto_{producto_id:02d}.jpg"
            ruta_imagen = f"/static/images/productos/{nombre_archivo}"
            
            # Actualizar en la base de datos
            cursor.execute("""
                UPDATE productos 
                SET imagen = ? 
                WHERE id = ?
            """, (ruta_imagen, producto_id))
            
            print(f"✓ Actualizado producto {producto_id}: {nombre} -> {ruta_imagen}")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n¡Actualizadas las rutas de {len(productos)} productos!")
        print("Ahora las imágenes usan rutas reales en /static/images/productos/")
        
    except Exception as e:
        print(f"Error al actualizar rutas: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    actualizar_imagenes_reales()
