#!/usr/bin/env python3
"""
Script para crear imágenes reales de productos de panadería
"""

import os
import sqlite3
from PIL import Image, ImageDraw, ImageFont

def crear_imagenes_productos():
    """Crea imágenes reales para los productos"""
    
    # Crear directorio si no existe
    images_dir = "app/static/images/productos"
    os.makedirs(images_dir, exist_ok=True)
    
    # Conectar a la base de datos
    conn = sqlite3.connect('panaderia.db')
    cursor = conn.cursor()
    
    try:
        # Obtener todos los productos
        cursor.execute("SELECT id, nombre, categoria_id FROM productos ORDER BY id")
        productos = cursor.fetchall()
        
        print("Creando imágenes de productos...")
        
        # Colores por categoría
        colores_categoria = {
            1: '#D2B48C',  # Panes - Beige
            2: '#8B4513',  # Pasteles - Marrón
            3: '#F4A460',  # Croissants - Arena
            4: '#DEB887',  # Galletas - Trigo
            5: '#CD853F'   # Especialidades - Dorado
        }
        
        for producto_id, nombre, categoria_id in productos:
            # Crear imagen
            img = Image.new('RGB', (400, 400), color=colores_categoria.get(categoria_id, '#F5F5DC'))
            draw = ImageDraw.Draw(img)
            
            # Dibujar círculo decorativo
            draw.ellipse([50, 50, 350, 350], fill='white', outline=colores_categoria.get(categoria_id, '#D2B48C'), width=3)
            
            # Agregar texto del nombre del producto
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Dividir nombre en líneas si es muy largo
            palabras = nombre.split()
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                if len(linea_actual + palabra) < 20:
                    linea_actual += palabra + " "
                else:
                    if linea_actual:
                        lineas.append(linea_actual.strip())
                    linea_actual = palabra + " "
            
            if linea_actual:
                lineas.append(linea_actual.strip())
            
            # Centrar texto
            y_start = 180 - (len(lineas) * 15)
            for i, linea in enumerate(lineas):
                bbox = draw.textbbox((0, 0), linea, font=font)
                text_width = bbox[2] - bbox[0]
                x = (400 - text_width) // 2
                y = y_start + (i * 30)
                draw.text((x, y), linea, fill='#8B4513', font=font)
            
            # Guardar imagen
            nombre_archivo = f"producto_{producto_id:02d}.jpg"
            ruta_completa = os.path.join(images_dir, nombre_archivo)
            img.save(ruta_completa, 'JPEG', quality=85)
            
            print(f"✓ Creada imagen: {nombre_archivo} para {nombre}")
        
        print(f"\n¡Creadas {len(productos)} imágenes de productos!")
        print(f"Imágenes guardadas en: {images_dir}")
        
    except Exception as e:
        print(f"Error al crear imágenes: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    crear_imagenes_productos()
