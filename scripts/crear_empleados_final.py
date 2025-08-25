#!/usr/bin/env python3
"""
Script final para crear usuarios empleados (Chef y Vendedor) correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('.'))))

from app.models.usuario import Usuario
import sqlite3

def crear_empleados_final():
    """Crear usuarios empleados de forma directa en la base de datos"""
    print("🧑‍🍳 Creando usuarios empleados...")
    
    # Conectar directamente a la base de datos
    conn = sqlite3.connect('panaderia.db')
    cursor = conn.cursor()
    
    # Hash de las contraseñas
    import hashlib
    chef_password = hashlib.sha256("chef123".encode()).hexdigest()
    vendedor_password = hashlib.sha256("venta123".encode()).hexdigest()
    
    empleados = [
        {
            'nombre': 'Carlos Mendoza',
            'email': 'chef@panaderia.com',
            'password': chef_password,
            'telefono': '555-0101',
            'direccion': 'Cocina Principal',
            'rol': 'chef'
        },
        {
            'nombre': 'Ana García',
            'email': 'vendedor@panaderia.com',
            'password': vendedor_password,
            'telefono': '555-0102',
            'direccion': 'Área de Ventas',
            'rol': 'vendedor'
        }
    ]
    
    for empleado in empleados:
        try:
            # Verificar si el usuario ya existe
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (empleado['email'],))
            if cursor.fetchone():
                print(f"⚠️  Usuario {empleado['email']} ya existe")
                continue
            
            # Insertar usuario directamente
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol, activo)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            ''', (empleado['nombre'], empleado['email'], empleado['password'], 
                  empleado['telefono'], empleado['direccion'], empleado['rol']))
            
            print(f"✓ Usuario {empleado['nombre']} ({empleado['rol']}) creado exitosamente")
            
        except Exception as e:
            print(f"❌ Error creando empleado {empleado['nombre']}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n🔐 CREDENCIALES DE EMPLEADOS:")
    print("   👨‍🍳 Chef:")
    print("      Email: chef@panaderia.com")
    print("      Contraseña: chef123")
    print()
    print("   👩‍💼 Vendedor:")
    print("      Email: vendedor@panaderia.com")
    print("      Contraseña: venta123")
    print()
    print("✅ Empleados creados correctamente!")

if __name__ == '__main__':
    crear_empleados_final()
