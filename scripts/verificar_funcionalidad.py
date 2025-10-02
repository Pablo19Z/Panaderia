#!/usr/bin/env python3
"""
Script para verificar que todas las funcionalidades estén trabajando correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.usuario import Usuario
from app.models.producto import Producto

def main():
    print("🔍 Verificando funcionalidad del sistema...")
    
    try:
        # Verificar usuarios
        print("\n👥 Verificando usuarios...")
        usuarios = Usuario.get_all()
        print(f"   Total usuarios: {len(usuarios)}")
        
        for usuario in usuarios:
            print(f"   - {usuario.nombre} ({usuario.email}) - Rol: {usuario.rol}")
        
        # Verificar productos
        print("\n📦 Verificando productos...")
        productos = Producto.get_all()
        print(f"   Total productos: {len(productos)}")
        
        if len(productos) > 0:
            print("   Primeros 3 productos:")
            for producto in productos[:3]:
                print(f"   - {producto.nombre} - ${producto.precio}")
        
        # Verificar login de usuario de prueba
        print("\n🔐 Verificando autenticación...")
        test_user = Usuario.find_by_email('admin@migasdeoro.com')
        if test_user:
            password_valid = test_user.verify_password('admin123')
            print(f"   Login admin: {'✅ OK' if password_valid else '❌ FALLO'}")
        else:
            print("   ❌ Usuario admin no encontrado")
        
        test_cliente = Usuario.find_by_email('cliente@test.com')
        if test_cliente:
            password_valid = test_cliente.verify_password('123456')
            print(f"   Login cliente: {'✅ OK' if password_valid else '❌ FALLO'}")
        else:
            print("   ❌ Usuario cliente no encontrado")
        
        print("\n✅ Verificación completada!")
        
    except Exception as e:
        print(f"❌ Error durante verificación: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
