import subprocess
import sys
import os

def ejecutar_actualizacion():
    """Ejecuta la actualización de precios y verifica los resultados"""
    
    print("🚀 INICIANDO ACTUALIZACIÓN DE PRECIOS A PESOS COLOMBIANOS")
    print("=" * 60)
    
    try:
        # Cambiar al directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Ejecutar actualización de precios
        print("📝 Ejecutando actualización de precios...")
        result = subprocess.run([sys.executable, "actualizar_precios_directamente.py"], 
                              capture_output=True, text=True, cwd=script_dir)
        
        if result.returncode == 0:
            print("✅ Actualización ejecutada exitosamente")
            print(result.stdout)
        else:
            print("❌ Error en la actualización:")
            print(result.stderr)
            return False
        
        print("\n" + "=" * 60)
        print("🔍 VERIFICANDO RESULTADOS...")
        
        # Verificar los precios actualizados
        result_verificacion = subprocess.run([sys.executable, "verificar_precios.py"], 
                                           capture_output=True, text=True, cwd=script_dir)
        
        if result_verificacion.returncode == 0:
            print(result_verificacion.stdout)
        else:
            print("❌ Error en la verificación:")
            print(result_verificacion.stderr)
            return False
        
        print("🎉 ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!")
        print("Los precios ahora están en pesos colombianos en toda la aplicación.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        return False

if __name__ == "__main__":
    ejecutar_actualizacion()
