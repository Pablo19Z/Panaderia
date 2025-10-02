#!/usr/bin/env python3
"""
Archivo principal para ejecutar la aplicación de la Panadería Migas de oro Dorè

Instrucciones de instalación:
1. Instalar Python 3.7 o superior
2. Instalar las dependencias: pip install -r requirements.txt
3. Ejecutar: python run.py

La aplicación estará disponible en: http://localhost:5093

Credenciales por defecto:
- Admin: admin@migasdeoro.com / admin123
- Vendedor: vendedor@migasdeoro.com / vendedor123
- Cliente: cliente@test.com / cliente123
"""

import os
import sys
import subprocess
import platform

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ Error: Se requiere Python 3.7 o superior")
        print(f"Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def instalar_dependencias():
    """Instala automáticamente las dependencias si no están disponibles"""
    dependencias = ['flask', 'flask-wtf', 'reportlab']
    dependencias_faltantes = []
    
    for dep in dependencias:
        try:
            if dep == 'flask-wtf':
                __import__('flask_wtf')
            else:
                __import__(dep)
            print(f"✓ {dep.capitalize()} ya está instalado")
        except ImportError:
            dependencias_faltantes.append(dep)
    
    if dependencias_faltantes:
        print(f"\n📦 Instalando dependencias faltantes: {', '.join(dependencias_faltantes)}")
        try:
            for dep in dependencias_faltantes:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                print(f"✓ {dep.capitalize()} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error al instalar dependencias: {e}")
            print("Intenta instalar manualmente: pip install flask flask-wtf reportlab")
            return False
    
    return True

def crear_directorios():
    """Crea los directorios necesarios para la aplicación"""
    directorios = [
        'app',
        'app/models',
        'app/routes', 
        'app/forms',
        'app/templates',
        'app/templates/auth',
        'app/templates/dashboard',
        'app/templates/productos',
        'app/templates/ventas',
        'app/templates/clientes',
        'app/templates/inventario',
        'app/templates/usuarios',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/images',
        'app/utils',
        'instance',
        'scripts'
    ]
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✓ Directorio creado: {directorio}")

def verificar_archivos():
    """Verifica que los archivos esenciales existan"""
    archivos_esenciales = [
        'app.py',
        'app/__init__.py',
        'config.py',
        'instance/config.py'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_esenciales:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"✗ Archivos faltantes: {', '.join(archivos_faltantes)}")
        return False
    
    print("✓ Todos los archivos esenciales están presentes")
    return True

def mostrar_informacion_sistema():
    """Muestra información del sistema"""
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Arquitectura: {platform.machine()}")
    print(f"Directorio de trabajo: {os.getcwd()}")

def abrir_navegador():
    """Intenta abrir el navegador automáticamente"""
    import webbrowser
    import time
    import threading
    
    def abrir_en_navegador():
        time.sleep(2)  # Esperar a que el servidor inicie
        try:
            webbrowser.open('http://localhost:5093')
            print("🌐 Navegador abierto automáticamente")
        except:
            pass
    
    thread = threading.Thread(target=abrir_en_navegador)
    thread.daemon = True
    thread.start()

def main():
    """Función principal para ejecutar la aplicación"""
    print("=" * 60)
    print("🥖 PANADERÍA MIGAS DE ORO DORÈ - SISTEMA WEB 🥖")
    print("=" * 60)
    print()
    
    # Mostrar información del sistema
    print("📋 Información del Sistema:")
    mostrar_informacion_sistema()
    print()
    
    # Verificar versión de Python
    print("🐍 Verificando Python...")
    if not verificar_python():
        input("Presiona Enter para salir...")
        sys.exit(1)
    print()
    
    # Instalar dependencias automáticamente
    print("📦 Verificando e instalando dependencias...")
    if not instalar_dependencias():
        input("Presiona Enter para salir...")
        sys.exit(1)
    print()
    
    # Crear directorios necesarios
    print("📁 Creando estructura de directorios...")
    crear_directorios()
    print()
    
    # Verificar archivos esenciales
    print("📄 Verificando archivos del proyecto...")
    if not verificar_archivos():
        print("✗ Faltan archivos esenciales del proyecto")
        input("Presiona Enter para salir...")
        sys.exit(1)
    print()
    
    # Inicializar base de datos
    print("🗄️ Inicializando base de datos SQLite...")
    try:
        from app.models import init_db
        init_db()
        print("✓ Base de datos SQLite inicializada correctamente")
        print("✓ Tablas creadas y datos de ejemplo insertados")
    except Exception as e:
        print(f"✗ Error al inicializar la base de datos: {e}")
        print("Intentando con método alternativo...")
        try:
            from database import db
            print("✓ Base de datos SQLite inicializada correctamente (método alternativo)")
        except Exception as e2:
            print(f"✗ Error crítico en base de datos: {e2}")
            input("Presiona Enter para salir...")
            sys.exit(1)
    print()
    
    # Mostrar credenciales por defecto
    print("🔐 CREDENCIALES POR DEFECTO:")
    print("   👤 Administrador:")
    print("      Email: admin@migasdeoro.com")
    print("      Contraseña: admin123")
    print()
    print("   💼 Vendedor:")
    print("      Email: vendedor@migasdeoro.com")
    print("      Contraseña: vendedor123")
    print()
    print("   👤 Cliente de prueba:")
    print("      Email: cliente@test.com") 
    print("      Contraseña: cliente123")
    print()

    # Ejecutar aplicación Flask
    print("🚀 Iniciando servidor web...")
    print("📍 URL: http://localhost:5093")
    print("🛑 Para detener el servidor presiona Ctrl+C")
    print("=" * 60)
    print()
    
    # Abrir navegador automáticamente
    abrir_navegador()
    
    try:
        from app import create_app
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5093, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
        print("¡Gracias por usar Migas de oro Dorè!")
    except Exception as e:
        print(f"\n✗ Error al ejecutar la aplicación: {e}")
        print("Verifica que el puerto 5093 no esté en uso")
        print("Intentando con método alternativo...")
        try:
            import app as app_module
            if hasattr(app_module, 'app'):
                app_module.app.run(debug=True, host='0.0.0.0', port=5093, use_reloader=False)
            else:
                print("✗ No se pudo encontrar la instancia de la aplicación")
                input("Presiona Enter para salir...")
                sys.exit(1)
        except Exception as e2:
            print(f"✗ Error crítico: {e2}")
            input("Presiona Enter para salir...")
            sys.exit(1)

if __name__ == '__main__':
    main()
