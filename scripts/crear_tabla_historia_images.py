import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.historia_images import HistoriaImages

def main():
    print("Creando tabla de imágenes de historia...")
    
    try:
        # Crear la tabla
        HistoriaImages.create_table()
        print("✓ Tabla historia_images creada exitosamente")
        
        # Inicializar valores por defecto
        HistoriaImages.initialize_defaults()
        print("✓ Valores por defecto inicializados")
        
        # Verificar
        images = HistoriaImages.get_all_images()
        print(f"\n✓ Total de imágenes configuradas: {len(images)}")
        print("\nImágenes disponibles:")
        for key, data in images.items():
            print(f"  - {key}: {data['description']}")
        
        print("\n¡Configuración completada exitosamente!")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
