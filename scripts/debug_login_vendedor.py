#!/usr/bin/env python3
"""
Script para debuggear el problema de login del vendedor
"""

import sqlite3
import hashlib
import os

def hash_password(password):
    """Hashea una contraseña usando el mismo método que la aplicación"""
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    print("🔍 Debuggeando login del vendedor...")
    
    # Verificar si existe la carpeta instance
    if not os.path.exists('instance'):
        os.makedirs('instance')
        print("📁 Carpeta 'instance' creada")
    
    # Conectar a la base de datos
    db_path = 'instance/panaderia.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar si existe el usuario vendedor
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", ('vendedor@migasdeoro.com',))
    vendedor = cursor.fetchone()
    
    if not vendedor:
        print("❌ Usuario vendedor no encontrado en la base de datos")
        print("🔧 Creando usuario vendedor...")
        
        # Crear usuario vendedor
        password_hash = hash_password('vendedor123')
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'Vendedor',  # Cambiando "Vendedor Principal" a solo "Vendedor"
            'vendedor@migasdeoro.com',
            password_hash,
            '555-0123',
            'Tienda Principal',
            'vendedor'
        ))
        conn.commit()
        print("✅ Usuario vendedor creado correctamente")
    else:
        print("✅ Usuario vendedor encontrado:")
        print(f"   ID: {vendedor[0]}")
        print(f"   Nombre: {vendedor[1]}")
        print(f"   Email: {vendedor[2]}")
        print(f"   Rol: {vendedor[6]}")
        print(f"   Activo: {vendedor[8]}")
        
        # Verificar contraseña
        stored_password = vendedor[3]
        expected_password = hash_password('vendedor123')
        
        print(f"\n🔐 Verificación de contraseña:")
        print(f"   Contraseña almacenada: {stored_password[:20]}...")
        print(f"   Contraseña esperada:   {expected_password[:20]}...")
        
        if stored_password == expected_password:
            print("✅ La contraseña es correcta")
        else:
            print("❌ La contraseña no coincide")
            print("🔧 Actualizando contraseña...")
            cursor.execute(
                "UPDATE usuarios SET password = ? WHERE email = ?",
                (expected_password, 'vendedor@migasdeoro.com')
            )
            conn.commit()
            print("✅ Contraseña actualizada")
    
    # Mostrar todos los usuarios para verificar
    print(f"\n📊 Usuarios en la base de datos:")
    cursor.execute("SELECT id, nombre, email, rol, activo FROM usuarios")
    usuarios = cursor.fetchall()
    
    for usuario in usuarios:
        status = "✅" if usuario[4] else "❌"
        print(f"   {status} {usuario[1]} ({usuario[2]}) - {usuario[3]}")
    
    conn.close()
    print(f"\n🎉 Debug completado. Intenta iniciar sesión nuevamente.")

if __name__ == "__main__":
    main()
