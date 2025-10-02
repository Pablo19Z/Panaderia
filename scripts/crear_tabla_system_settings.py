import sqlite3
import os
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from instance.config import InstanceConfig

def crear_tabla_system_settings():
    """Crea la tabla system_settings en la base de datos"""
    
    print("Creando tabla system_settings...")
    
    conn = sqlite3.connect(InstanceConfig.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Crear tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar configuración por defecto para hero_background_url
    cursor.execute('''
        INSERT OR IGNORE INTO system_settings (key, value, description)
        VALUES (?, ?, ?)
    ''', ('hero_background_url', '/placeholder.svg?height=600&width=1200', 'URL de la imagen de fondo del hero en la página de inicio'))
    
    conn.commit()
    
    # Verificar que se creó correctamente
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='system_settings'")
    if cursor.fetchone():
        print("✓ Tabla system_settings creada exitosamente")
        
        cursor.execute("SELECT * FROM system_settings")
        settings = cursor.fetchall()
        print(f"✓ Configuraciones iniciales: {len(settings)}")
        for setting in settings:
            print(f"  - {setting[1]}: {setting[2]}")
    else:
        print("✗ Error al crear la tabla")
    
    conn.close()

if __name__ == '__main__':
    crear_tabla_system_settings()
