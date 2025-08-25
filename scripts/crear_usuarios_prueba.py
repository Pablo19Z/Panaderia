#!/usr/bin/env python3
"""
Script para crear usuarios de prueba con diferentes roles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

def crear_usuarios_prueba():
    """Crea usuarios de prueba para todos los roles"""
    
    usuarios_prueba = [
        {
            'nombre': 'Vendedor Prueba',
            'email': 'vendedor@migasdeoro.com',
            'password': 'vendedor123',
            'rol': 'vendedor',
            'telefono': '555-0001',
            'direccion': 'Panadería Migas de Oro'
        },
        {
            'nombre': 'Chef Principal',
            'email': 'chef@migasdeoro.com',
            'password': 'chef123',
            'rol': 'chef',
            'telefono': '555-0002',
            'direccion': 'Panadería Migas de Oro'
        },
        {
            'nombre': 'Cocinero Prueba',
            'email': 'cocinero@migasdeoro.com',
            'password': 'cocinero123',
            'rol': 'cocinero',
            'telefono': '555-0003',
            'direccion': 'Panadería Migas de Oro'
        }
    ]
    
    print("Creando usuarios de prueba...")
    
    for usuario_data in usuarios_prueba:
        try:
            # Verificar si el usuario ya existe
            if Usuario.find_by_email(usuario_data['email']):
                print(f"✓ Usuario {usuario_data['email']} ya existe")
                continue
            
            # Crear usuario
            usuario_id = Usuario.create(usuario_data)
            print(f"✓ Usuario {usuario_data['nombre']} ({usuario_data['rol']}) creado con ID: {usuario_id}")
            
        except Exception as e:
            print(f"✗ Error creando usuario {usuario_data['email']}: {str(e)}")
    
    print("\n=== CREDENCIALES DE ACCESO ===")
    print("- Admin: admin@migasdeoro.com / admin123")
    print("- Cliente: cliente@test.com / cliente123")
    print("- Vendedor: vendedor@migasdeoro.com / vendedor123")
    print("- Chef: chef@migasdeoro.com / chef123")
    print("- Cocinero: cocinero@migasdeoro.com / cocinero123")

if __name__ == '__main__':
    crear_usuarios_prueba()
