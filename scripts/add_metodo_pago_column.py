import sqlite3
import os

def add_metodo_pago_column():
    """Agrega la columna metodo_pago a la tabla pedidos si no existe"""
    
    # Obtener la ruta de la base de datos
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'panaderia.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la columna metodo_pago ya existe
        cursor.execute("PRAGMA table_info(pedidos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'metodo_pago' not in columns:
            print("Agregando columna metodo_pago a la tabla pedidos...")
            cursor.execute("ALTER TABLE pedidos ADD COLUMN metodo_pago TEXT DEFAULT 'efectivo'")
            conn.commit()
            print("✓ Columna metodo_pago agregada exitosamente")
        else:
            print("✓ La columna metodo_pago ya existe")
        
        conn.close()
        print("✓ Migración completada")
        
    except Exception as e:
        print(f"❌ Error al agregar la columna: {e}")

if __name__ == "__main__":
    add_metodo_pago_column()
