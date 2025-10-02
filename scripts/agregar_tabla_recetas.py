"""
Script de migración para agregar la tabla de recetas a bases de datos existentes.
Ejecutar este script si ya tienes una base de datos y quieres agregar la funcionalidad de recetas.
"""

import sqlite3
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from instance.config import InstanceConfig

def agregar_tabla_recetas():
    """Agrega la tabla de recetas a la base de datos existente"""
    
    print("🔧 Iniciando migración: Agregar tabla de recetas...")
    
    try:
        conn = sqlite3.connect(InstanceConfig.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='recetas'
        """)
        
        if cursor.fetchone():
            print("⚠️  La tabla 'recetas' ya existe. No se requiere migración.")
            conn.close()
            return
        
        # Crear tabla de recetas
        print("📝 Creando tabla 'recetas'...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                ingredientes TEXT,
                instrucciones TEXT,
                tiempo_preparacion INTEGER,
                porciones INTEGER,
                dificultad TEXT,
                imagen TEXT,
                categoria_id INTEGER,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        
        conn.commit()
        print("✅ Tabla 'recetas' creada exitosamente.")
        
        # Agregar recetas de ejemplo
        print("📚 Agregando recetas de ejemplo...")
        
        recetas_ejemplo = [
            (
                "Pan Francés Tradicional",
                "Receta clásica de pan francés con corteza crujiente",
                "- 500g de harina de trigo\n- 300ml de agua tibia\n- 10g de levadura fresca\n- 10g de sal\n- 5g de azúcar",
                "1. Disolver la levadura en agua tibia con azúcar\n2. Mezclar la harina con la sal\n3. Agregar el agua con levadura y amasar 10 minutos\n4. Dejar reposar 1 hora hasta duplicar tamaño\n5. Formar los panes y hacer cortes en la superficie\n6. Hornear a 220°C por 25-30 minutos",
                120, 4, "Media", None, 1
            ),
            (
                "Croissant de Mantequilla",
                "Croissants hojaldrados con mantequilla francesa",
                "- 500g de harina\n- 250ml de leche\n- 50g de azúcar\n- 20g de levadura\n- 250g de mantequilla fría\n- 10g de sal",
                "1. Preparar masa base con harina, leche, azúcar, levadura y sal\n2. Refrigerar 30 minutos\n3. Laminar la mantequilla entre la masa\n4. Realizar 3 dobleces simples refrigerando entre cada uno\n5. Estirar y cortar triángulos\n6. Enrollar y hornear a 200°C por 15-18 minutos",
                240, 12, "Difícil", None, 1
            ),
            (
                "Torta de Chocolate",
                "Torta húmeda de chocolate con cobertura de ganache",
                "- 200g de harina\n- 200g de azúcar\n- 100g de cacao en polvo\n- 3 huevos\n- 150ml de aceite\n- 200ml de leche\n- 1 cucharadita de polvo de hornear",
                "1. Batir huevos con azúcar hasta espumar\n2. Agregar aceite y leche\n3. Incorporar harina, cacao y polvo de hornear tamizados\n4. Verter en molde engrasado\n5. Hornear a 180°C por 35-40 minutos\n6. Dejar enfriar y cubrir con ganache",
                60, 8, "Fácil", None, 2
            )
        ]
        
        cursor.executemany('''
            INSERT INTO recetas (nombre, descripcion, ingredientes, instrucciones, 
                               tiempo_preparacion, porciones, dificultad, imagen, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', recetas_ejemplo)
        
        conn.commit()
        print(f"✅ Se agregaron {len(recetas_ejemplo)} recetas de ejemplo.")
        
        conn.close()
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("📖 Ahora puedes gestionar recetas desde el panel de administrador.")
        print("🔗 Accede a: /admin/recetas")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        sys.exit(1)

if __name__ == '__main__':
    agregar_tabla_recetas()
