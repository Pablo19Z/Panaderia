#!/usr/bin/env python3
"""
Script para actualizar el constraint de la tabla usuarios eliminando 'cocinero'
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import get_db_connection

def main():
    print("🔄 Actualizando constraint de tabla usuarios...")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear nueva tabla con constraint actualizado
        cursor.execute('''
            CREATE TABLE usuarios_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                telefono TEXT,
                direccion TEXT,
                rol TEXT DEFAULT 'cliente' CHECK(rol IN ('cliente', 'admin', 'vendedor', 'chef')),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Copiar datos de la tabla original
        cursor.execute('''
            INSERT INTO usuarios_new 
            SELECT * FROM usuarios
        ''')
        
        # Eliminar tabla original
        cursor.execute('DROP TABLE usuarios')
        
        # Renombrar nueva tabla
        cursor.execute('ALTER TABLE usuarios_new RENAME TO usuarios')
        
        conn.commit()
        conn.close()
        
        print("✅ Constraint de tabla usuarios actualizado correctamente")
        print("🎉 Rol 'cocinero' eliminado del sistema!")
        
    except Exception as e:
        print(f"❌ Error al actualizar constraint: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
