#!/usr/bin/env python3
"""
Script para crear usuarios empleados (Chef y Vendedor) en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db_connection
from app.models.usuario import Usuario
from app.models.chef import Chef
from app.models.vendedor import Vendedor

def crear_usuarios_empleados():
    """Crear usuarios empleados de prueba"""
    print("🧑‍🍳 Creando usuarios empleados...")
    
    # Crear tablas si no existen
    Chef.create_table()
    Vendedor.create_table()
    
    # Datos de empleados
    empleados = [
        {
            'tipo': 'chef',
            'usuario': {
                'nombre': 'Carlos Mendoza',
                'email': 'chef@panaderia.com',
                'password': 'chef123',
                'telefono': '555-0101',
                'direccion': 'Cocina Principal',
                'rol': 'chef'
            },
            'perfil': {
                'especialidad': 'Panadería Artesanal',
                'experiencia_anos': 8,
                'certificaciones': 'Certificado en Panadería Francesa, Especialista en Masas',
                'salario': 3500000
            }
        },
        {
            'tipo': 'vendedor',
            'usuario': {
                'nombre': 'Ana García',
                'email': 'vendedor@panaderia.com',
                'password': 'venta123',
                'telefono': '555-0102',
                'direccion': 'Área de Ventas',
                'rol': 'vendedor'
            },
            'perfil': {
                'zona_asignada': 'Centro Comercial',
                'meta_mensual': 2000000,
                'comision_porcentaje': 7.5
            }
        }
    ]
    
    for empleado in empleados:
        try:
            # Verificar si el usuario ya existe
            usuario_existente = Usuario.find_by_email(empleado['usuario']['email'])
            
            if usuario_existente:
                print(f"⚠️  Usuario {empleado['usuario']['email']} ya existe")
                usuario_id = usuario_existente.id
            else:
                # Crear usuario
                usuario_id = Usuario.create(empleado['usuario'])
                print(f"✓ Usuario {empleado['usuario']['nombre']} creado")
            
            # Crear perfil específico
            if empleado['tipo'] == 'chef':
                chef_existente = Chef.find_by_usuario_id(usuario_id)
                if not chef_existente:
                    empleado['perfil']['usuario_id'] = usuario_id
                    Chef.create(empleado['perfil'])
                    print(f"✓ Perfil de Chef creado para {empleado['usuario']['nombre']}")
                else:
                    print(f"⚠️  Perfil de Chef ya existe para {empleado['usuario']['nombre']}")
                    
            elif empleado['tipo'] == 'vendedor':
                vendedor_existente = Vendedor.find_by_usuario_id(usuario_id)
                if not vendedor_existente:
                    empleado['perfil']['usuario_id'] = usuario_id
                    Vendedor.create(empleado['perfil'])
                    print(f"✓ Perfil de Vendedor creado para {empleado['usuario']['nombre']}")
                else:
                    print(f"⚠️  Perfil de Vendedor ya existe para {empleado['usuario']['nombre']}")
                    
        except Exception as e:
            print(f"❌ Error creando empleado {empleado['usuario']['nombre']}: {e}")
    
    print("\n🔐 CREDENCIALES DE EMPLEADOS:")
    print("   👨‍🍳 Chef:")
    print("      Email: chef@panaderia.com")
    print("      Contraseña: chef123")
    print()
    print("   👩‍💼 Vendedor:")
    print("      Email: vendedor@panaderia.com")
    print("      Contraseña: venta123")
    print()

if __name__ == '__main__':
    crear_usuarios_empleados()
