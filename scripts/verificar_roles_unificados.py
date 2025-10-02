#!/usr/bin/env python3
"""
Script para verificar que los roles admin y administrador funcionan correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.usuario import Usuario
from app.models.roles import Roles

def verificar_roles_unificados():
    """Verifica que ambos roles admin y administrador tengan los mismos permisos"""
    
    print("🔍 Verificando unificación de roles admin y administrador...")
    
    # Verificar roles disponibles
    roles_disponibles = Roles.get_roles_disponibles()
    print(f"\n📋 Roles disponibles: {roles_disponibles}")
    
    # Verificar que ambos roles existen
    admin_existe = 'admin' in roles_disponibles
    administrador_existe = 'administrador' in roles_disponibles
    
    print(f"   • Rol 'admin' disponible: {admin_existe}")
    print(f"   • Rol 'administrador' disponible: {administrador_existe}")
    
    if not (admin_existe and administrador_existe):
        print("❌ Error: Faltan roles en la configuración")
        return False
    
    # Comparar permisos
    permisos_admin = Roles.get_permisos_rol('admin')
    permisos_administrador = Roles.get_permisos_rol('administrador')
    
    print(f"\n🔐 Comparación de permisos:")
    print(f"   Permisos 'admin': {len(permisos_admin)} permisos")
    print(f"   Permisos 'administrador': {len(permisos_administrador)} permisos")
    
    # Verificar que tienen los mismos permisos
    permisos_iguales = set(permisos_admin) == set(permisos_administrador)
    print(f"   Permisos idénticos: {permisos_iguales}")
    
    if not permisos_iguales:
        print("❌ Error: Los permisos no son idénticos")
        print(f"   Solo en admin: {set(permisos_admin) - set(permisos_administrador)}")
        print(f"   Solo en administrador: {set(permisos_administrador) - set(permisos_admin)}")
        return False
    
    # Verificar permisos específicos importantes
    permisos_importantes = [
        'gestionar_productos',
        'gestionar_usuarios',
        'gestionar_categorias',
        'ver_todas_estadisticas'
    ]
    
    print(f"\n✅ Verificación de permisos importantes:")
    for permiso in permisos_importantes:
        admin_tiene = Roles.usuario_tiene_permiso('admin', permiso)
        administrador_tiene = Roles.usuario_tiene_permiso('administrador', permiso)
        
        print(f"   • {permiso}:")
        print(f"     - admin: {admin_tiene}")
        print(f"     - administrador: {administrador_tiene}")
        
        if admin_tiene != administrador_tiene:
            print(f"❌ Error: Permiso '{permiso}' no coincide entre roles")
            return False
    
    # Verificar función es_rol_administrativo
    print(f"\n🔧 Verificación de función es_rol_administrativo:")
    admin_es_administrativo = Roles.es_rol_administrativo('admin')
    administrador_es_administrativo = Roles.es_rol_administrativo('administrador')
    
    print(f"   • admin es administrativo: {admin_es_administrativo}")
    print(f"   • administrador es administrativo: {administrador_es_administrativo}")
    
    if not (admin_es_administrativo and administrador_es_administrativo):
        print("❌ Error: Función es_rol_administrativo no funciona correctamente")
        return False
    
    # Verificar usuarios existentes
    print(f"\n👥 Usuarios con roles administrativos:")
    usuarios = Usuario.get_all()
    admins_encontrados = 0
    administradores_encontrados = 0
    
    for usuario in usuarios:
        if usuario.rol == 'admin':
            admins_encontrados += 1
            print(f"   • {usuario.nombre} ({usuario.email}) - rol: admin")
        elif usuario.rol == 'administrador':
            administradores_encontrados += 1
            print(f"   • {usuario.nombre} ({usuario.email}) - rol: administrador")
    
    print(f"\n📊 Resumen:")
    print(f"   • Usuarios con rol 'admin': {admins_encontrados}")
    print(f"   • Usuarios con rol 'administrador': {administradores_encontrados}")
    print(f"   • Total usuarios administrativos: {admins_encontrados + administradores_encontrados}")
    
    print(f"\n✅ Verificación completada exitosamente!")
    print(f"   Los roles 'admin' y 'administrador' están correctamente unificados.")
    
    return True

if __name__ == "__main__":
    verificar_roles_unificados()
