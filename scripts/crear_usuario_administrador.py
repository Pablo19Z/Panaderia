#!/usr/bin/env python3
"""
Script para crear un usuario con rol 'administrador' para probar la funcionalidad unificada
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.usuario import Usuario
from app.models import get_db_connection

def crear_usuario_administrador():
    """Crea un usuario con rol administrador para pruebas"""
    
    print("🔧 Creando usuario administrador...")
    
    # Datos del usuario administrador
    datos_admin = {
        'nombre': 'Administrador Principal',
        'email': 'administrador@migasdeoro.com',
        'password': 'admin123',
        'telefono': '+57 300 123 4567',
        'direccion': 'Oficina Principal - Migas de Oro',
        'rol': 'administrador'
    }
    
    try:
        # Verificar si ya existe
        usuario_existente = Usuario.find_by_email(datos_admin['email'])
        if usuario_existente:
            print(f"⚠️  Usuario administrador ya existe: {usuario_existente.email}")
            print(f"   Rol actual: {usuario_existente.rol}")
            return
        
        # Crear usuario administrador
        usuario_id = Usuario.create(datos_admin)
        print(f"✅ Usuario administrador creado exitosamente!")
        print(f"   ID: {usuario_id}")
        print(f"   Email: {datos_admin['email']}")
        print(f"   Rol: {datos_admin['rol']}")
        print(f"   Password: {datos_admin['password']}")
        
        # Verificar permisos
        from app.models.roles import Roles
        permisos = Roles.get_permisos_rol('administrador')
        print(f"\n📋 Permisos del rol 'administrador':")
        for permiso in permisos:
            print(f"   • {permiso}")
            
        print(f"\n🔐 Verificación de acceso administrativo:")
        print(f"   Es rol administrativo: {Roles.es_rol_administrativo('administrador')}")
        print(f"   Puede gestionar productos: {Roles.usuario_tiene_permiso('administrador', 'gestionar_productos')}")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        return False
    
    return True

if __name__ == "__main__":
    crear_usuario_administrador()
