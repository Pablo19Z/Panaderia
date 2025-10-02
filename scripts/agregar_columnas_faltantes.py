import sqlite3
import os

def agregar_columnas_faltantes():
    """
    Agrega las columnas faltantes a la tabla pedidos:
    - fecha_entrega: Fecha programada para la entrega
    - hora_entrega: Hora programada para la entrega
    - comprobante_pago: Ruta o URL del comprobante de pago
    """
    
    # Obtener la ruta de la base de datos
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'panaderia.db')
    
    print("=" * 60)
    print("🔧 MIGRACIÓN: Agregar columnas faltantes a tabla pedidos")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar qué columnas existen actualmente
        cursor.execute("PRAGMA table_info(pedidos)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        print(f"\n📋 Columnas actuales en tabla pedidos:")
        for col in columnas_existentes:
            print(f"   ✓ {col}")
        
        columnas_a_agregar = []
        
        # Agregar fecha_entrega si no existe
        if 'fecha_entrega' not in columnas_existentes:
            columnas_a_agregar.append(('fecha_entrega', 'DATE'))
            
        # Agregar hora_entrega si no existe
        if 'hora_entrega' not in columnas_existentes:
            columnas_a_agregar.append(('hora_entrega', 'TIME'))
            
        # Agregar comprobante_pago si no existe
        if 'comprobante_pago' not in columnas_existentes:
            columnas_a_agregar.append(('comprobante_pago', 'TEXT'))
        
        if not columnas_a_agregar:
            print("\n✅ Todas las columnas ya existen. No se requiere migración.")
            conn.close()
            return
        
        print(f"\n🔨 Agregando {len(columnas_a_agregar)} columna(s) faltante(s):")
        
        for columna, tipo in columnas_a_agregar:
            try:
                cursor.execute(f"ALTER TABLE pedidos ADD COLUMN {columna} {tipo}")
                print(f"   ✓ Columna '{columna}' ({tipo}) agregada exitosamente")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"   ⚠️  Columna '{columna}' ya existe (omitiendo)")
                else:
                    raise
        
        conn.commit()
        
        # Verificar las columnas después de la migración
        cursor.execute("PRAGMA table_info(pedidos)")
        columnas_finales = [col[1] for col in cursor.fetchall()]
        
        print(f"\n📋 Columnas finales en tabla pedidos:")
        for col in columnas_finales:
            print(f"   ✓ {col}")
        
        print("\n✅ Migración completada exitosamente")
        print("=" * 60)
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    agregar_columnas_faltantes()
