#!/usr/bin/env python3
"""
Script para inicializar la base de datos SQLite directamente
"""

import sqlite3
import hashlib
import os
from datetime import datetime

def verificar_password(password, hashed_password):
    """Verificar si la contraseña coincide con el hash"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

def main():
    print("🔧 Inicializando base de datos SQLite...")
    
    try:
        os.makedirs('instance', exist_ok=True)
        db_path = 'instance/panaderia.db'
        
        # Eliminar base de datos anterior si existe en la raíz
        if os.path.exists('panaderia.db'):
            os.remove('panaderia.db')
            print("🗑️  Base de datos anterior eliminada de la raíz")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📋 Creando tablas...")
        
        # Crear tabla usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                telefono TEXT,
                direccion TEXT,
                rol TEXT NOT NULL CHECK(rol IN ('cliente', 'vendedor', 'chef', 'admin')),
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                categoria TEXT,
                imagen_url TEXT,
                disponible BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Crear tabla pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                total REAL NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                direccion_entrega TEXT,
                telefono_contacto TEXT,
                notas TEXT,
                metodo_pago TEXT DEFAULT 'efectivo',
                fecha_entrega DATE,
                hora_entrega TIME,
                comprobante_pago TEXT,
                fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Crear tabla carrito
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrito (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER DEFAULT 1,
                fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        print("✅ Tablas creadas correctamente")
        
        # Crear usuarios de prueba
        usuarios_prueba = [
            {
                'nombre': 'Administrador',
                'email': 'admin@migasdeoro.com',
                'password': 'admin123',
                'telefono': '123-456-7890',
                'direccion': 'Calle Principal 123',
                'rol': 'admin'
            },
            {
                'nombre': 'Vendedor',
                'email': 'vendedor@migasdeoro.com',
                'password': 'vendedor123',
                'telefono': '555-0123',
                'direccion': 'Tienda Principal',
                'rol': 'vendedor'
            },
            {
                'nombre': 'Chef Principal',
                'email': 'chef@migasdeoro.com',
                'password': 'chef123',
                'telefono': '555-0456',
                'direccion': 'Cocina Principal',
                'rol': 'chef'
            },
            {
                'nombre': 'Cliente Prueba',
                'email': 'cliente@test.com',
                'password': '123456',
                'telefono': '987-654-3210',
                'direccion': 'Avenida Test 456',
                'rol': 'cliente'
            }
        ]
        
        for usuario in usuarios_prueba:
            # Verificar si el usuario ya existe
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (usuario['email'],))
            existing = cursor.fetchone()
            
            if not existing:
                # Hashear la contraseña
                password_hash = hashlib.sha256(usuario['password'].encode()).hexdigest()
                
                # Insertar usuario
                cursor.execute('''
                    INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                ''', (
                    usuario['nombre'],
                    usuario['email'],
                    password_hash,
                    usuario['telefono'],
                    usuario['direccion'],
                    usuario['rol']
                ))
                
                user_id = cursor.lastrowid
                print(f"✅ Usuario {usuario['rol']} creado con ID: {user_id}")
                
                # Si es cliente, crear entrada en tabla clientes
                if usuario['rol'] == 'cliente':
                    cursor.execute('''
                        INSERT INTO clientes (usuario_id, fecha_registro)
                        VALUES (?, datetime('now'))
                    ''', (user_id,))
            else:
                print(f"ℹ️  Usuario {usuario['rol']} ya existe")
        
        # Crear algunos productos de ejemplo
        productos_ejemplo = [
            {
                'nombre': 'Pan Integral',
                'descripcion': 'Pan integral artesanal con semillas',
                'precio': 2.50,
                'categoria': 'Panes',
                'imagen_url': '/static/images/pan-integral.jpg'
            },
            {
                'nombre': 'Croissant de Mantequilla',
                'descripcion': 'Croissant francés con mantequilla fresca',
                'precio': 1.80,
                'categoria': 'Bollería',
                'imagen_url': '/static/images/croissant.jpg'
            },
            {
                'nombre': 'Tarta de Chocolate',
                'descripcion': 'Deliciosa tarta de chocolate con crema',
                'precio': 15.00,
                'categoria': 'Postres',
                'imagen_url': '/static/images/tarta-chocolate.jpg'
            }
        ]
        
        for producto in productos_ejemplo:
            cursor.execute('SELECT id FROM productos WHERE nombre = ?', (producto['nombre'],))
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute('''
                    INSERT INTO productos (nombre, descripcion, precio, categoria, imagen_url, disponible, fecha_creacion)
                    VALUES (?, ?, ?, ?, ?, 1, datetime('now'))
                ''', (
                    producto['nombre'],
                    producto['descripcion'],
                    producto['precio'],
                    producto['categoria'],
                    producto['imagen_url']
                ))
                print(f"✅ Producto '{producto['nombre']}' creado")
            else:
                print(f"ℹ️  Producto '{producto['nombre']}' ya existe")
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar datos
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        total_usuarios = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM productos')
        total_productos = cursor.fetchone()[0]
        
        print(f"\n📊 Resumen:")
        print(f"   👥 Total usuarios: {total_usuarios}")
        print(f"   📦 Total productos: {total_productos}")
        print(f"   📁 Base de datos creada en: {db_path}")
        
        print("\n🎉 Base de datos inicializada correctamente!")
        print("\n📝 Credenciales de prueba:")
        print("   👑 Admin: admin@migasdeoro.com / admin123")
        print("   💼 Vendedor: vendedor@migasdeoro.com / vendedor123")
        print("   👨‍🍳 Chef: chef@migasdeoro.com / chef123")
        print("   👤 Cliente: cliente@test.com / 123456")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    main()
