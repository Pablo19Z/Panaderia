#!/usr/bin/env python3
"""
Script para migrar usuarios con rol 'cocinero' a 'chef' o eliminarlos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import get_db_connection

def main():
    print("🔄 Migrando usuarios con rol 'cocinero'...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar usuarios con rol cocinero
        cursor.execute("SELECT id, nombre, email FROM usuarios WHERE rol = 'cocinero' AND activo = 1")
        usuarios_cocinero = cursor.fetchall()
        
        if not usuarios_cocinero:
            print("ℹ️  No se encontraron usuarios con rol 'cocinero'")
            return True
        
        print(f"📋 Encontrados {len(usuarios_cocinero)} usuarios con rol 'cocinero':")
        for usuario in usuarios_cocinero:
            print(f"   - ID: {usuario[0]}, Nombre: {usuario[1]}, Email: {usuario[2]}")
        
        # Migrar usuarios cocinero a chef
        cursor.execute("UPDATE usuarios SET rol = 'chef' WHERE rol = 'cocinero'")
        usuarios_migrados = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ {usuarios_migrados} usuarios migrados de 'cocinero' a 'chef'")
        print("🎉 Migración completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
