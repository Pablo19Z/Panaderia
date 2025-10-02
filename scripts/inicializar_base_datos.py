#!/usr/bin/env python3
"""
Script para inicializar la base de datos y crear usuarios de prueba
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.usuario import Usuario
from app.models.producto import Producto
from app.models.cliente import Cliente

def main():
    print("🔧 Inicializando base de datos...")
    
    try:
        # Crear tablas
        print("📋 Creando tablas...")
        Usuario.create_table()
        Producto.create_table()
        Cliente.create_table()
        
        # Crear usuario admin de prueba
        print("👤 Creando usuario administrador...")
        admin_data = {
            'nombre': 'Administrador',
            'email': 'admin@migasdeoro.com',
            'password': 'admin123',
            'telefono': '123-456-7890',
            'direccion': 'Calle Principal 123',
            'rol': 'admin'
        }
        
        # Verificar si ya existe
        existing_admin = Usuario.find_by_email(admin_data['email'])
        if not existing_admin:
            admin_id = Usuario.create(admin_data)
            print(f"✅ Usuario admin creado con ID: {admin_id}")
        else:
            print("ℹ️  Usuario admin ya existe")
        
        print("👤 Creando usuario vendedor...")
        vendedor_data = {
            'nombre': 'Vendedor',
            'email': 'vendedor@migasdeoro.com',
            'password': 'vendedor123',
            'telefono': '555-0123',
            'direccion': 'Tienda Principal',
            'rol': 'vendedor'
        }
        
        existing_vendedor = Usuario.find_by_email(vendedor_data['email'])
        if not existing_vendedor:
            vendedor_id = Usuario.create(vendedor_data)
            print(f"✅ Usuario vendedor creado con ID: {vendedor_id}")
        else:
            print("ℹ️  Usuario vendedor ya existe")
        
        # Crear usuario cliente de prueba
        print("👤 Creando usuario cliente...")
        cliente_data = {
            'nombre': 'Cliente Prueba',
            'email': 'cliente@test.com',
            'password': '123456',
            'telefono': '987-654-3210',
            'direccion': 'Avenida Test 456',
            'rol': 'cliente'
        }
        
        existing_cliente = Usuario.find_by_email(cliente_data['email'])
        if not existing_cliente:
            cliente_id = Usuario.create(cliente_data)
            print(f"✅ Usuario cliente creado con ID: {cliente_id}")
        else:
            print("ℹ️  Usuario cliente ya existe")
        
        # Verificar productos
        productos = Producto.get_all()
        print(f"📦 Productos en base de datos: {len(productos)}")
        
        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📝 Credenciales de prueba:")
        print("   Admin: admin@migasdeoro.com / admin123")
        print("   Vendedor: vendedor@migasdeoro.com / vendedor123")
        print("   Cliente: cliente@test.com / 123456")
        
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
