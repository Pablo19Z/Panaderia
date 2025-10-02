#!/usr/bin/env python3
"""
Script para resetear la base de datos eliminando el archivo antiguo
"""

import os
import sys

def main():
    print("🔄 RESETEAR BASE DE DATOS")
    print("=" * 60)
    print("Este script eliminará la base de datos actual y permitirá")
    print("que se cree una nueva con el esquema correcto.")
    print("=" * 60)
    
    # Rutas posibles de la base de datos
    db_paths = [
        'instance/panaderia.db',
        'panaderia.db'
    ]
    
    eliminados = 0
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"✅ Base de datos eliminada: {db_path}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error al eliminar {db_path}: {e}")
                print("   Asegúrate de que la aplicación esté cerrada.")
                return False
        else:
            print(f"ℹ️  No existe: {db_path}")
    
    if eliminados > 0:
        print("\n🎉 Base de datos eliminada correctamente!")
        print("\n📝 SIGUIENTE PASO:")
        print("   Ejecuta 'python run.py' para crear la base de datos")
        print("   con el esquema correcto y todas las columnas necesarias.")
        print("\n✨ Después de esto, las compras funcionarán perfectamente!")
        return True
    else:
        print("\n⚠️  No se encontró ninguna base de datos para eliminar.")
        print("   Ejecuta 'python run.py' para crear una nueva.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
