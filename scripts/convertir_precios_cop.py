#!/usr/bin/env python3
"""
Script para convertir todos los precios de productos de USD a pesos colombianos (COP)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from datetime import datetime

def convertir_precios_a_cop():
    """Convierte todos los precios de productos a pesos colombianos"""
    
    # Tasa de cambio aproximada USD a COP (actualizar según tasa actual)
    TASA_CAMBIO_USD_COP = 4200  # 1 USD = 4200 COP aproximadamente
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('instance/panaderia.db')
        cursor = conn.cursor()
        
        # Obtener todos los productos actuales
        cursor.execute("SELECT id, nombre, precio FROM productos WHERE activo = 1")
        productos = cursor.fetchall()
        
        print(f"🔄 Convirtiendo precios de {len(productos)} productos a pesos colombianos...")
        print(f"💱 Tasa de cambio utilizada: 1 USD = {TASA_CAMBIO_USD_COP:,} COP")
        print("=" * 70)
        
        productos_actualizados = 0
        
        for producto_id, nombre, precio_usd in productos:
            # Convertir precio a COP y redondear a múltiplos de 100
            precio_cop = round(precio_usd * TASA_CAMBIO_USD_COP / 100) * 100
            
            # Actualizar precio en la base de datos
            cursor.execute(
                "UPDATE productos SET precio = ? WHERE id = ?",
                (precio_cop, producto_id)
            )
            
            print(f"✓ {nombre:<35} ${precio_usd:>6.2f} USD → ${precio_cop:>8,.0f} COP")
            productos_actualizados += 1
        
        # Confirmar cambios
        conn.commit()
        
        print("=" * 70)
        print(f"✅ {productos_actualizados} productos actualizados exitosamente")
        print(f"💰 Todos los precios ahora están en pesos colombianos (COP)")
        
        # Mostrar resumen de precios actualizados
        cursor.execute("""
            SELECT c.nombre as categoria, p.nombre, p.precio 
            FROM productos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id 
            WHERE p.activo = 1 
            ORDER BY c.nombre, p.precio DESC
        """)
        
        productos_actualizados = cursor.fetchall()
        
        print("\n📋 CATÁLOGO ACTUALIZADO (PRECIOS EN COP):")
        print("=" * 70)
        
        categoria_actual = None
        for categoria, nombre, precio in productos_actualizados:
            if categoria_actual != categoria:
                categoria_actual = categoria
                print(f"\n🏷️  {categoria.upper() if categoria else 'SIN CATEGORÍA'}")
                print("-" * 50)
            
            print(f"   • {nombre:<35} ${precio:>8,.0f} COP")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al convertir precios: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

def verificar_conversion():
    """Verifica que la conversión se haya realizado correctamente"""
    try:
        conn = sqlite3.connect('instance/panaderia.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT MIN(precio), MAX(precio), AVG(precio) FROM productos WHERE activo = 1")
        min_precio, max_precio, avg_precio = cursor.fetchone()
        
        print(f"\n📊 ESTADÍSTICAS DE PRECIOS:")
        print(f"   Precio mínimo: ${min_precio:,.0f} COP")
        print(f"   Precio máximo: ${max_precio:,.0f} COP") 
        print(f"   Precio promedio: ${avg_precio:,.0f} COP")
        
        # Verificar que los precios están en rango esperado de COP
        if min_precio > 1000 and max_precio > 10000:
            print("✅ Los precios parecen estar correctamente convertidos a COP")
        else:
            print("⚠️  Los precios podrían no estar en el formato COP esperado")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al verificar conversión: {e}")

if __name__ == '__main__':
    print("💰 Conversión de Precios a Pesos Colombianos")
    print("=" * 50)
    print("Este script convertirá todos los precios de USD a COP")
    
    respuesta = input("\n¿Continuar con la conversión? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        convertir_precios_a_cop()
        verificar_conversion()
        print("\n🎉 ¡Conversión completada exitosamente!")
        print("Los PDFs y la aplicación ahora mostrarán precios en pesos colombianos.")
    else:
        print("❌ Conversión cancelada por el usuario")
