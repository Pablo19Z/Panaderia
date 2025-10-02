"""
Script para eliminar todas las recetas existentes y agregar las 6 recetas específicas.
Ejecutar este script para reemplazar las recetas actuales con las 6 recetas de la panadería.
"""

import sqlite3
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from instance.config import InstanceConfig

def actualizar_recetas():
    """Elimina todas las recetas y agrega las 6 específicas"""
    
    print("🔧 Iniciando actualización de recetas...")
    
    try:
        conn = sqlite3.connect(InstanceConfig.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='recetas'
        """)
        
        if not cursor.fetchone():
            print("❌ La tabla 'recetas' no existe. Ejecuta primero 'agregar_tabla_recetas.py'")
            conn.close()
            return
        
        # Eliminar todas las recetas existentes
        print("🗑️  Eliminando recetas existentes...")
        cursor.execute("DELETE FROM recetas")
        conn.commit()
        print("✅ Recetas anteriores eliminadas.")
        
        # Agregar las 6 recetas específicas
        print("📚 Agregando las 6 recetas específicas...")
        
        # Obtener el ID de la categoría "Panadería" (asumiendo que existe)
        cursor.execute("SELECT id FROM categorias WHERE nombre LIKE '%Panadería%' OR nombre LIKE '%Pan%' LIMIT 1")
        categoria_result = cursor.fetchone()
        categoria_id = categoria_result[0] if categoria_result else 1
        
        recetas_especificas = [
            (
                "Muffins de Arándanos",
                "Muffins esponjosos con arándanos frescos, perfectos para el desayuno.",
                "- 250g de harina de trigo\n- 150g de azúcar\n- 2 huevos\n- 120ml de leche\n- 80ml de aceite vegetal\n- 150g de arándanos frescos\n- 1 cucharadita de polvo de hornear\n- 1 pizca de sal\n- Ralladura de 1 limón",
                "1. Precalentar el horno a 180°C y preparar moldes para muffins\n2. Mezclar harina, azúcar, polvo de hornear y sal en un bowl\n3. En otro bowl, batir huevos, leche, aceite y ralladura de limón\n4. Incorporar los ingredientes secos a los húmedos sin batir demasiado\n5. Agregar los arándanos con movimientos suaves\n6. Rellenar los moldes hasta 3/4 de su capacidad\n7. Hornear por 20-25 minutos hasta que estén dorados\n8. Dejar enfriar antes de desmoldar",
                25, 12, "Fácil", "/placeholder.svg?height=300&width=400", categoria_id
            ),
            (
                "Brownies de Chocolate",
                "Brownies húmedos y chocolatosos, irresistibles para los amantes del chocolate.",
                "- 200g de chocolate oscuro\n- 150g de mantequilla\n- 200g de azúcar\n- 3 huevos\n- 100g de harina\n- 30g de cacao en polvo\n- 1 pizca de sal\n- 100g de nueces (opcional)",
                "1. Precalentar el horno a 180°C y engrasar un molde cuadrado\n2. Derretir el chocolate con la mantequilla a baño maría\n3. Retirar del fuego y agregar el azúcar, mezclar bien\n4. Incorporar los huevos uno a uno, batiendo después de cada adición\n5. Tamizar la harina, cacao y sal, e incorporar a la mezcla\n6. Agregar las nueces picadas si se desea\n7. Verter en el molde y hornear por 30-35 minutos\n8. El centro debe quedar ligeramente húmedo\n9. Dejar enfriar completamente antes de cortar en cuadrados",
                35, 16, "Fácil", "/placeholder.svg?height=300&width=400", categoria_id
            ),
            (
                "Cookies de Avena",
                "Cookies caseras de avena, crujientes y llenas de sabor tradicional.",
                "- 150g de harina de trigo\n- 150g de avena en hojuelas\n- 120g de mantequilla\n- 100g de azúcar morena\n- 50g de azúcar blanca\n- 1 huevo\n- 1 cucharadita de vainilla\n- 1/2 cucharadita de bicarbonato\n- 1 pizca de sal\n- 100g de chips de chocolate (opcional)",
                "1. Precalentar el horno a 180°C y forrar bandejas con papel mantequilla\n2. Batir la mantequilla con ambos azúcares hasta obtener una crema\n3. Agregar el huevo y la vainilla, batir bien\n4. Incorporar la harina, avena, bicarbonato y sal\n5. Agregar los chips de chocolate si se desea\n6. Formar bolitas de masa y colocar en las bandejas con espacio entre ellas\n7. Aplanar ligeramente con un tenedor\n8. Hornear por 12-15 minutos hasta que los bordes estén dorados\n9. Dejar enfriar en la bandeja 5 minutos antes de transferir",
                20, 24, "Fácil", "/placeholder.svg?height=300&width=400", categoria_id
            ),
            (
                "Pancakes Esponjosos",
                "Pancakes súper esponjosos y dorados, perfectos para un desayuno especial.",
                "- 200g de harina de trigo\n- 2 cucharadas de azúcar\n- 2 cucharaditas de polvo de hornear\n- 1/2 cucharadita de sal\n- 250ml de leche\n- 1 huevo\n- 30g de mantequilla derretida\n- 1 cucharadita de vainilla",
                "1. Mezclar en un bowl la harina, azúcar, polvo de hornear y sal\n2. En otro bowl, batir el huevo con la leche, mantequilla y vainilla\n3. Incorporar los ingredientes húmedos a los secos con movimientos envolventes\n4. No batir demasiado, algunos grumos están bien\n5. Calentar una sartén antiadherente a fuego medio\n6. Verter 1/4 taza de mezcla por cada pancake\n7. Cocinar hasta que aparezcan burbujas en la superficie (2-3 minutos)\n8. Voltear y cocinar 1-2 minutos más hasta dorar\n9. Servir calientes con miel, jarabe de maple o frutas",
                15, 8, "Fácil", "/placeholder.svg?height=300&width=400", categoria_id
            ),
            (
                "Cupcakes de Vainilla",
                "Cupcakes suaves de vainilla con frosting cremoso, ideales para celebraciones.",
                "- 150g de harina de trigo\n- 150g de azúcar\n- 100g de mantequilla\n- 2 huevos\n- 100ml de leche\n- 1 cucharadita de polvo de hornear\n- 2 cucharaditas de extracto de vainilla\n- 1 pizca de sal\n\nPara el frosting:\n- 200g de mantequilla\n- 400g de azúcar glass\n- 2 cucharadas de leche\n- 1 cucharadita de vainilla",
                "1. Precalentar el horno a 180°C y colocar capacillos en moldes para cupcakes\n2. Batir la mantequilla con el azúcar hasta obtener una crema esponjosa\n3. Agregar los huevos uno a uno, batiendo bien después de cada uno\n4. Incorporar la vainilla\n5. Mezclar la harina, polvo de hornear y sal\n6. Alternar la adición de ingredientes secos y leche a la mezcla\n7. Rellenar los capacillos hasta 2/3 de su capacidad\n8. Hornear por 18-20 minutos hasta que al insertar un palillo salga limpio\n9. Dejar enfriar completamente\n10. Para el frosting: batir mantequilla, agregar azúcar glass gradualmente, leche y vainilla\n11. Decorar los cupcakes con manga pastelera",
                30, 12, "Fácil", "/placeholder.svg?height=300&width=400", categoria_id
            ),
            (
                "Pan de Banana",
                "Pan húmedo y aromático de banana, perfecto para aprovechar bananas maduras.",
                "- 3 bananas maduras\n- 200g de harina de trigo\n- 150g de azúcar\n- 2 huevos\n- 80ml de aceite vegetal\n- 1 cucharadita de polvo de hornear\n- 1/2 cucharadita de bicarbonato\n- 1 cucharadita de canela\n- 1 pizca de sal\n- 100g de nueces picadas (opcional)",
                "1. Precalentar el horno a 180°C y engrasar un molde para pan\n2. Triturar las bananas con un tenedor hasta obtener un puré\n3. Batir los huevos con el azúcar hasta que estén espumosos\n4. Agregar el aceite y el puré de banana, mezclar bien\n5. Tamizar la harina, polvo de hornear, bicarbonato, canela y sal\n6. Incorporar los ingredientes secos a la mezcla húmeda\n7. Agregar las nueces si se desea\n8. Verter la mezcla en el molde preparado\n9. Hornear por 50-60 minutos hasta que al insertar un palillo salga limpio\n10. Dejar enfriar en el molde 10 minutos antes de desmoldar\n11. Enfriar completamente antes de cortar",
                60, 8, "Fácil", "/placeholder.svg?height=300&width=400", categoria_id
            )
        ]
        
        cursor.executemany('''
            INSERT INTO recetas (nombre, descripcion, ingredientes, instrucciones, 
                               tiempo_preparacion, porciones, dificultad, imagen, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', recetas_especificas)
        
        conn.commit()
        print(f"✅ Se agregaron las 6 recetas específicas exitosamente.")
        
        # Mostrar las recetas agregadas
        cursor.execute("SELECT id, nombre, tiempo_preparacion, porciones FROM recetas")
        recetas = cursor.fetchall()
        
        print("\n📋 Recetas en la base de datos:")
        for receta in recetas:
            print(f"   • {receta[1]} - {receta[2]} min - {receta[3]} porciones")
        
        conn.close()
        
        print("\n🎉 ¡Actualización completada exitosamente!")
        print("📖 Las 6 recetas están listas para gestionar desde el panel de administrador.")
        print("🔗 Accede a: /admin/recetas")
        
    except Exception as e:
        print(f"\n❌ Error durante la actualización: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        sys.exit(1)

if __name__ == '__main__':
    actualizar_recetas()
