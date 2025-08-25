#!/usr/bin/env python3
"""
Script para crear imágenes placeholder más específicas para los productos
"""

import os
import sqlite3

def crear_imagenes_productos():
    """Crea archivos de referencia para las imágenes de productos basados en la base de datos"""
    
    # Crear directorios si no existen
    images_dir = 'app/static/images/productos'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # Conectar a la base de datos para obtener los productos reales
    try:
        conn = sqlite3.connect('panaderia.db')
        cursor = conn.cursor()
        
        # Obtener todos los productos
        cursor.execute("SELECT id, nombre, categoria_id FROM productos ORDER BY id")
        productos = cursor.fetchall()
        
        print(f"📸 Creando imágenes para {len(productos)} productos...")
        
        for producto_id, nombre, categoria_id in productos:
            # Generar nombre de archivo basado en el ID
            nombre_archivo = f"producto_{producto_id:02d}.jpg"
            
            # Crear query específico para cada tipo de producto
            query_map = {
                1: "fresh artisan bread loaf",  # Panes
                2: "delicious chocolate cake",   # Pasteles
                3: "golden butter croissant",   # Croissants
                4: "homemade chocolate cookies", # Galletas
                5: "specialty bakery item"      # Especialidades
            }
            
            query = query_map.get(categoria_id, "bakery product")
            
            # Crear archivo de referencia con URL placeholder específica
            archivo_path = os.path.join(images_dir, f"{nombre_archivo}.txt")
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(f"Producto: {nombre}\n")
                f.write(f"ID: {producto_id}\n")
                f.write(f"Archivo: {nombre_archivo}\n")
                f.write(f"URL Placeholder: /placeholder.svg?height=400&width=400&query={query}\n")
                f.write(f"Ruta en DB: /static/images/productos/{nombre_archivo}\n")
            
            print(f"✓ Creada referencia para: {nombre}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
        print("Creando imágenes genéricas...")
        
        # Crear imágenes genéricas si no hay base de datos
        for i in range(1, 16):
            nombre_archivo = f"producto_{i:02d}.jpg"
            archivo_path = os.path.join(images_dir, f"{nombre_archivo}.txt")
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(f"Producto genérico #{i}\n")
                f.write(f"Archivo: {nombre_archivo}\n")
                f.write(f"URL Placeholder: /placeholder.svg?height=400&width=400&query=bakery product\n")
                f.write(f"Ruta en DB: /static/images/productos/{nombre_archivo}\n")
    
    print(f"✓ Referencias de imágenes creadas en {images_dir}")
    
    # Crear también imágenes para categorías
    categorias_dir = 'app/static/images/categorias'
    if not os.path.exists(categorias_dir):
        os.makedirs(categorias_dir)
    
    imagenes_categorias = {
        'panes.jpg': 'fresh artisan bread collection',
        'pasteles.jpg': 'delicious cakes and pastries',
        'croissants.jpg': 'golden butter croissants',
        'galletas.jpg': 'homemade cookies variety',
        'especialidades.jpg': 'specialty bakery items'
    }
    
    for nombre_archivo, query in imagenes_categorias.items():
        archivo_path = os.path.join(categorias_dir, f"{nombre_archivo}.txt")
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(f"Categoría: {nombre_archivo.replace('.jpg', '').title()}\n")
            f.write(f"Archivo: {nombre_archivo}\n")
            f.write(f"URL Placeholder: /placeholder.svg?height=300&width=400&query={query}\n")
            f.write(f"Ruta en DB: /static/images/categorias/{nombre_archivo}\n")
    
    print(f"✓ {len(imagenes_categorias)} referencias de categorías creadas en {categorias_dir}")

if __name__ == '__main__':
    print("📸 Creando referencias de imágenes para productos")
    print("=" * 50)
    
    crear_imagenes_productos()
    
    print("\n🎉 ¡Referencias de imágenes creadas exitosamente!")
    print("Las imágenes placeholder se mostrarán automáticamente en la aplicación.")
    print("Para usar imágenes reales, reemplaza los archivos .txt con archivos .jpg reales.")
