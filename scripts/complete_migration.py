import sqlite3
import os

def complete_migration():
    """Agrega todas las columnas faltantes a la tabla pedidos"""
    
    # Obtener la ruta de la base de datos
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'panaderia.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar qué columnas existen
        cursor.execute("PRAGMA table_info(pedidos)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        print(f"Columnas existentes: {existing_columns}")
        
        # Lista de columnas que necesitamos
        required_columns = {
            'metodo_pago': 'TEXT DEFAULT "efectivo"',
            'fecha_entrega': 'TEXT',
            'hora_entrega': 'TEXT'
        }
        
        # Agregar columnas faltantes
        for column_name, column_definition in required_columns.items():
            if column_name not in existing_columns:
                print(f"Agregando columna {column_name}...")
                cursor.execute(f"ALTER TABLE pedidos ADD COLUMN {column_name} {column_definition}")
                conn.commit()
                print(f"✓ Columna {column_name} agregada exitosamente")
            else:
                print(f"✓ La columna {column_name} ya existe")
        
        conn.close()
        print("✓ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")

if __name__ == "__main__":
    complete_migration()
