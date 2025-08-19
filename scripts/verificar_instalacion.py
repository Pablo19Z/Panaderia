#!/usr/bin/env python3
"""
Script de verificación de instalación para Migas de oro Dorè
Ejecuta pruebas básicas para asegurar que todo funcione correctamente
"""

import os
import sys
import sqlite3

def verificar_base_datos():
    """Verifica que la base de datos esté correctamente configurada"""
    print("🗄️ Verificando base de datos...")
    
    try:
        # Verificar que el archivo de base de datos existe
        if not os.path.exists('panaderia.db'):
            print("✗ Archivo de base de datos no encontrado")
            return False
        
        # Conectar y verificar tablas
        conn = sqlite3.connect('panaderia.db')
        cursor = conn.cursor()
        
        # Verificar tablas principales
        tablas_requeridas = [
            'usuarios', 'productos', 'categorias', 'carrito', 
            'favoritos', 'pedidos', 'resenas', 'mensajes_chatbot', 'insumos'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]
        
        for tabla in tablas_requeridas:
            if tabla in tablas_existentes:
                print(f"✓ Tabla '{tabla}' encontrada")
            else:
                print(f"✗ Tabla '{tabla}' faltante")
                conn.close()
                return False
        
        # Verificar datos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM productos")
        productos_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM categorias")
        categorias_count = cursor.fetchone()[0]
        
        print(f"✓ Usuarios en BD: {usuarios_count}")
        print(f"✓ Productos en BD: {productos_count}")
        print(f"✓ Categorías en BD: {categorias_count}")
        
        conn.close()
        
        if usuarios_count > 0 and productos_count > 0 and categorias_count > 0:
            print("✓ Base de datos configurada correctamente")
            return True
        else:
            print("✗ Base de datos sin datos de ejemplo")
            return False
            
    except Exception as e:
        print(f"✗ Error al verificar base de datos: {e}")
        return False

def verificar_archivos_templates():
    """Verifica que las plantillas HTML existan"""
    print("\n📄 Verificando plantillas HTML...")
    
    templates_requeridos = [
        'templates/base.html',
        'templates/index.html',
        'templates/productos.html',
        'templates/carrito.html',
        'templates/chatbot.html',
        'templates/auth/login.html',
        'templates/auth/register.html',
        'templates/dashboards/cliente.html',
        'templates/dashboards/admin.html'
    ]
    
    todos_ok = True
    for template in templates_requeridos:
        if os.path.exists(template):
            print(f"✓ {template}")
        else:
            print(f"✗ {template} - FALTANTE")
            todos_ok = False
    
    return todos_ok

def verificar_estructura_directorios():
    """Verifica la estructura de directorios"""
    print("\n📁 Verificando estructura de directorios...")
    
    directorios_requeridos = [
        'static',
        'static/images',
        'templates',
        'templates/auth',
        'templates/dashboards'
    ]
    
    todos_ok = True
    for directorio in directorios_requeridos:
        if os.path.exists(directorio):
            print(f"✓ {directorio}/")
        else:
            print(f"✗ {directorio}/ - FALTANTE")
            todos_ok = False
    
    return todos_ok

def verificar_importaciones():
    """Verifica que los módulos se puedan importar correctamente"""
    print("\n🐍 Verificando importaciones de módulos...")
    
    try:
        import flask
        print("✓ Flask importado correctamente")
        
        from database import db
        print("✓ Módulo database importado correctamente")
        
        from app import app
        print("✓ Aplicación Flask importada correctamente")
        
        return True
        
    except ImportError as e:
        print(f"✗ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"✗ Error general: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE INSTALACIÓN - MIGAS DE ORO DORÈ")
    print("=" * 60)
    
    verificaciones = [
        verificar_estructura_directorios(),
        verificar_archivos_templates(),
        verificar_importaciones(),
        verificar_base_datos()
    ]
    
    print("\n" + "=" * 60)
    
    if all(verificaciones):
        print("🎉 ¡VERIFICACIÓN EXITOSA!")
        print("✅ Todos los componentes están correctamente instalados")
        print("🚀 La aplicación está lista para ejecutarse")
        print("\nPara iniciar la aplicación ejecuta: python run.py")
    else:
        print("❌ VERIFICACIÓN FALLIDA")
        print("⚠️ Algunos componentes tienen problemas")
        print("🔧 Revisa los errores mostrados arriba")
        print("\nIntenta ejecutar: python run.py (puede auto-reparar algunos problemas)")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
