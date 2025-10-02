#!/usr/bin/env python3
"""
Script para mantener solo las 6 recetas específicas y eliminar cualquier otra
"""
import sqlite3
import os

def mantener_solo_6_recetas():
    # Ruta a la base de datos
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'panaderia.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos en {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Nombres de las 6 recetas que queremos mantener
        recetas_mantener = [
            'Muffins de Arándanos',
            'Brownies de Chocolate',
            'Cookies de Avena',
            'Pancakes Esponjosos',
            'Cupcakes de Vainilla',
            'Pan de Banana'
        ]
        
        # Obtener todas las recetas actuales
        cursor.execute("SELECT id, nombre FROM recetas")
        todas_recetas = cursor.fetchall()
        
        print(f"\n📊 Recetas encontradas en la base de datos: {len(todas_recetas)}")
        
        # Identificar recetas a eliminar
        recetas_eliminar = []
        recetas_existentes = []
        
        for receta_id, nombre in todas_recetas:
            if nombre in recetas_mantener:
                recetas_existentes.append(nombre)
                print(f"✅ Manteniendo: {nombre}")
            else:
                recetas_eliminar.append((receta_id, nombre))
                print(f"🗑️  Eliminando: {nombre}")
        
        # Eliminar recetas que no están en la lista
        if recetas_eliminar:
            for receta_id, nombre in recetas_eliminar:
                cursor.execute("DELETE FROM recetas WHERE id = ?", (receta_id,))
            conn.commit()
            print(f"\n✅ Se eliminaron {len(recetas_eliminar)} recetas extras")
        else:
            print("\n✅ No hay recetas extras para eliminar")
        
        # Verificar si faltan recetas de las 6
        recetas_faltantes = [r for r in recetas_mantener if r not in recetas_existentes]
        
        if recetas_faltantes:
            print(f"\n⚠️  Advertencia: Faltan {len(recetas_faltantes)} recetas:")
            for nombre in recetas_faltantes:
                print(f"   - {nombre}")
        else:
            print(f"\n✅ Las 6 recetas están completas")
        
        # Mostrar resumen final
        cursor.execute("SELECT COUNT(*) FROM recetas")
        total_final = cursor.fetchone()[0]
        print(f"\n📊 Total de recetas en la base de datos: {total_final}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Manteniendo solo las 6 recetas específicas...")
    print("=" * 60)
    
    if mantener_solo_6_recetas():
        print("\n✅ Proceso completado exitosamente")
        print("\n📝 Ahora puedes:")
        print("   1. Reiniciar la aplicación")
        print("   2. Ir a 'Gestionar Recetas' para ver las 6 recetas")
        print("   3. Agregar nuevas recetas desde 'Nueva Receta'")
    else:
        print("\n❌ El proceso falló. Revisa los errores arriba.")
