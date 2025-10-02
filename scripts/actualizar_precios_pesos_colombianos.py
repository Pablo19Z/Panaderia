#!/usr/bin/env python3
"""
Script para actualizar todos los precios a pesos colombianos realistas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3

def actualizar_precios_pesos():
    """Actualiza todos los precios a pesos colombianos realistas"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('instance/panaderia.db')
    cursor = conn.cursor()
    
    # Mapeo de precios realistas en pesos colombianos
    precios_pesos = {
        'Pan Francés': 2500,
        'Pan Francés Artesanal': 2500,
        'Croissant': 3000,
        'Croissant de Mantequilla': 3500,
        'Croissant de mantequilla artesanal': 3000,
        'Torta de Chocolate': 32000,
        'Torta de Chocolate Belga': 32000,
        'Galletas de Avena': 1500,
        'Galletas de Chocolate Chip': 1500,
        'Cookies de Avena y Pasas': 1800,
        'Pan Integral con Semillas': 3200,
        'Baguette Tradicional': 2800,
        'Cheesecake de Frutos Rojos': 28000,
        'Torta Red Velvet': 35000,
        'Croissant de Almendras': 4500,
        'Pain au Chocolat': 4000,
        'Macarons Franceses': 2500,
        'Pan de Oro Dorè Especial': 12000,
        'Empanadas Gourmet': 5500,
        'Strudel de Manzana': 8500
    }
    
    try:
        # Obtener todos los productos actuales
        cursor.execute("SELECT id, nombre, precio FROM productos WHERE activo = 1")
        productos = cursor.fetchall()
        
        print("🔄 Actualizando precios a pesos colombianos...")
        print("=" * 50)
        
        productos_actualizados = 0
        
        for producto_id, nombre, precio_actual in productos:
            # Buscar precio exacto o similar
            nuevo_precio = None
            
            # Buscar coincidencia exacta
            if nombre in precios_pesos:
                nuevo_precio = precios_pesos[nombre]
            else:
                # Buscar coincidencia parcial
                for nombre_precio, precio in precios_pesos.items():
                    if nombre_precio.lower() in nombre.lower() or nombre.lower() in nombre_precio.lower():
                        nuevo_precio = precio
                        break
            
            # Si no encuentra coincidencia, convertir usando tasa aproximada
            if nuevo_precio is None:
                # Tasa aproximada: 1 USD = 4000 COP
                nuevo_precio = int(precio_actual * 4000)
                # Redondear a múltiplos de 100
                nuevo_precio = round(nuevo_precio / 100) * 100
            
            # Actualizar en la base de datos
            cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, producto_id))
            
            print(f"✓ {nombre:<30} ${precio_actual:>6.2f} → ${nuevo_precio:>8,}")
            productos_actualizados += 1
        
        conn.commit()
        
        print("=" * 50)
        print(f"✅ {productos_actualizados} productos actualizados exitosamente")
        
        # Mostrar resumen final
        cursor.execute("SELECT nombre, precio FROM productos WHERE activo = 1 ORDER BY precio DESC")
        productos_finales = cursor.fetchall()
        
        print("\n📋 PRECIOS FINALES EN PESOS COLOMBIANOS:")
        print("=" * 50)
        for nombre, precio in productos_finales:
            print(f"   • {nombre:<30} ${precio:>8,}")
        
    except Exception as e:
        print(f"❌ Error al actualizar precios: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("💰 Actualizando precios a pesos colombianos")
    print("🥖 Migas de oro Dorè - Conversión de precios")
    print("=" * 50)
    
    actualizar_precios_pesos()
    
    print("\n🎉 ¡Conversión completada!")
    print("Todos los precios ahora están en pesos colombianos realistas.")
