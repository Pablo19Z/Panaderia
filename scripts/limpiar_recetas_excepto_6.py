#!/usr/bin/env python3
"""
Script para eliminar todas las recetas EXCEPTO las 6 específicas que ya existen.
Mantiene solo: Muffins de Arándanos, Brownies de Chocolate, Cookies de Avena,
Pancakes Esponjosos, Cupcakes de Vainilla, Pan de Banana
"""

import sqlite3
import os

# Nombres exactos de las 6 recetas a mantener
RECETAS_A_MANTENER = [
    'Muffins de Arándanos',
    'Brownies de Chocolate',
    'Cookies de Avena',
    'Pancakes Esponjosos',
    'Cupcakes de Vainilla',
    'Pan de Banana'
]

def limpiar_recetas():
    """Elimina todas las recetas excepto las 6 especificadas"""
    
    # Ruta a la base de datos
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'panaderia.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos en {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar que la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recetas'")
        if not cursor.fetchone():
            print("❌ Error: La tabla 'recetas' no existe")
            conn.close()
            return False
        
        # Contar recetas antes
        cursor.execute("SELECT COUNT(*) FROM recetas")
        total_antes = cursor.fetchone()[0]
        print(f"\n📊 Total de recetas antes: {total_antes}")
        
        # Mostrar las recetas que se mantendrán
        placeholders = ','.join('?' * len(RECETAS_A_MANTENER))
        cursor.execute(f"SELECT id, nombre FROM recetas WHERE nombre IN ({placeholders})", RECETAS_A_MANTENER)
        recetas_mantener = cursor.fetchall()
        
        print(f"\n✅ Recetas que se mantendrán ({len(recetas_mantener)}):")
        for receta_id, nombre in recetas_mantener:
            print(f"   - {nombre} (ID: {receta_id})")
        
        # Eliminar todas las recetas que NO estén en la lista
        cursor.execute(f"DELETE FROM recetas WHERE nombre NOT IN ({placeholders})", RECETAS_A_MANTENER)
        eliminadas = cursor.rowcount
        
        conn.commit()
        
        # Contar recetas después
        cursor.execute("SELECT COUNT(*) FROM recetas")
        total_despues = cursor.fetchone()[0]
        
        print(f"\n🗑️  Recetas eliminadas: {eliminadas}")
        print(f"📊 Total de recetas después: {total_despues}")
        
        conn.close()
        
        print("\n✅ Limpieza completada exitosamente!")
        print("💡 Reinicia la aplicación para ver los cambios")
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧹 LIMPIEZA DE RECETAS - Mantener solo 6 específicas")
    print("=" * 60)
    
    respuesta = input("\n⚠️  ¿Estás seguro de eliminar todas las recetas excepto las 6 específicas? (s/n): ")
    
    if respuesta.lower() == 's':
        limpiar_recetas()
    else:
        print("\n❌ Operación cancelada")
