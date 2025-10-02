#!/usr/bin/env python3
"""
Script para agregar productos de ejemplo con imágenes a la panadería
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.producto import Producto
from app.models.categoria import Categoria
import sqlite3

def agregar_productos_ejemplo():
    """Agrega productos de ejemplo a la base de datos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('instance/panaderia.db')
    cursor = conn.cursor()
    
    # Productos de panadería con descripciones detalladas
    productos_ejemplo = [
        # Panes
        {
            'nombre': 'Pan Francés Artesanal',
            'descripcion': 'Pan tradicional francés elaborado con masa madre natural, corteza crujiente y miga suave. Perfecto para acompañar cualquier comida.',
            'precio': 2.50,
            'categoria_id': 1,
            'stock': 25,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Pan Integral con Semillas',
            'descripcion': 'Pan nutritivo elaborado con harina integral y una mezcla especial de semillas de girasol, sésamo y chía. Rico en fibra y proteínas.',
            'precio': 3.00,
            'categoria_id': 1,
            'stock': 20,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Baguette Tradicional',
            'descripcion': 'Auténtica baguette francesa con corteza dorada y crujiente, miga alveolada. Elaborada siguiendo la receta tradicional parisina.',
            'precio': 2.75,
            'categoria_id': 1,
            'stock': 30,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        
        # Pasteles
        {
            'nombre': 'Torta de Chocolate Belga',
            'descripcion': 'Exquisita torta de chocolate belga con tres capas, relleno de ganache y cobertura de chocolate semi-amargo. Un verdadero placer.',
            'precio': 25.00,
            'categoria_id': 2,
            'stock': 8,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Cheesecake de Frutos Rojos',
            'descripcion': 'Cremoso cheesecake sobre base de galleta, coronado con una selección de frutos rojos frescos y coulis de frambuesa.',
            'precio': 22.00,
            'categoria_id': 2,
            'stock': 6,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Torta Red Velvet',
            'descripcion': 'Clásica torta red velvet con su característico color rojo, suave textura aterciopelada y frosting de queso crema.',
            'precio': 28.00,
            'categoria_id': 2,
            'stock': 5,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        
        # Croissants
        {
            'nombre': 'Croissant de Mantequilla',
            'descripción': 'Croissant francés tradicional con capas hojaldradas, elaborado con mantequilla francesa de primera calidad. Crujiente por fuera, suave por dentro.',
            'precio': 3.50,
            'categoria_id': 3,
            'stock': 40,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Croissant de Almendras',
            'descripcion': 'Delicioso croissant relleno de crema de almendras, cubierto con almendras laminadas y azúcar glas. Una delicia francesa.',
            'precio': 4.25,
            'categoria_id': 3,
            'stock': 25,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Pain au Chocolat',
            'descripcion': 'Croissant relleno con barras de chocolate semi-amargo, masa hojaldrada perfecta. El desayuno favorito de Francia.',
            'precio': 3.75,
            'categoria_id': 3,
            'stock': 35,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        
        # Galletas
        {
            'nombre': 'Galletas de Chocolate Chip',
            'descripcion': 'Galletas caseras con chips de chocolate belga, textura crujiente por fuera y suave por dentro. Receta familiar secreta.',
            'precio': 1.50,
            'categoria_id': 4,
            'stock': 60,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Macarons Franceses',
            'descripcion': 'Delicados macarons franceses en variedad de sabores: vainilla, chocolate, frambuesa y pistacho. Presentación elegante.',
            'precio': 2.00,
            'categoria_id': 4,
            'stock': 48,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Cookies de Avena y Pasas',
            'descripcion': 'Galletas nutritivas de avena con pasas sultanas, canela y nuez moscada. Perfectas para acompañar el té o café.',
            'precio': 1.75,
            'categoria_id': 4,
            'stock': 45,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        
        # Especialidades
        {
            'nombre': 'Pan de Oro Dorè Especial',
            'descripcion': 'Nuestra especialidad de la casa: pan artesanal con semillas doradas, miel de abeja y un toque de azafrán. Receta exclusiva.',
            'precio': 8.50,
            'categoria_id': 5,
            'stock': 12,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Empanadas Gourmet',
            'descripcion': 'Empanadas artesanales con rellenos gourmet: carne a la criolla, pollo al curry, espinaca y ricotta. Masa casera.',
            'precio': 4.50,
            'categoria_id': 5,
            'stock': 24,
            'imagen': '/placeholder.svg?height=300&width=300'
        },
        {
            'nombre': 'Strudel de Manzana',
            'descripcion': 'Tradicional strudel austriaco con manzanas caramelizadas, canela, nueces y masa filo crujiente. Servido tibio.',
            'precio': 6.75,
            'categoria_id': 5,
            'stock': 10,
            'imagen': '/placeholder.svg?height=300&width=300'
        }
    ]
    
    try:
        for producto in productos_ejemplo:
            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, precio, categoria_id, stock, imagen, activo)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            ''', (
                producto['nombre'],
                producto['descripcion'], 
                producto['precio'],
                producto['categoria_id'],
                producto['stock'],
                producto['imagen']
            ))
        
        conn.commit()
        print(f"✓ {len(productos_ejemplo)} productos agregados exitosamente")
        
        # Mostrar resumen
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
        total_productos = cursor.fetchone()[0]
        print(f"✓ Total de productos en catálogo: {total_productos}")
        
    except Exception as e:
        print(f"✗ Error al agregar productos: {e}")
        conn.rollback()
    finally:
        conn.close()

def mostrar_productos():
    """Muestra todos los productos en la base de datos"""
    conn = sqlite3.connect('instance/panaderia.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.nombre, p.precio, c.nombre as categoria, p.stock
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.activo = 1
        ORDER BY c.nombre, p.nombre
    ''')
    
    productos = cursor.fetchall()
    
    print("\n📋 CATÁLOGO DE PRODUCTOS:")
    print("=" * 60)
    
    categoria_actual = None
    for producto in productos:
        if categoria_actual != producto[2]:
            categoria_actual = producto[2]
            print(f"\n🏷️  {categoria_actual.upper()}")
            print("-" * 40)
        
        print(f"   • {producto[0]:<30} ${producto[1]:>6.2f} (Stock: {producto[3]})")
    
    print(f"\n✓ Total de productos: {len(productos)}")
    conn.close()

if __name__ == '__main__':
    print("🥖 Agregando productos de ejemplo a Migas de oro Dorè")
    print("=" * 50)
    
    agregar_productos_ejemplo()
    mostrar_productos()
    
    print("\n🎉 ¡Productos agregados exitosamente!")
    print("Ejecuta 'python run.py' para ver la aplicación con los nuevos productos.")
