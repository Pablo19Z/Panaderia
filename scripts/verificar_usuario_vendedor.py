#!/usr/bin/env python3
"""
Script para verificar y recrear el usuario vendedor si es necesario
"""

import sqlite3
import hashlib
import os

def verificar_password(password, hashed_password):
    """Verificar si la contraseña coincide con el hash"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

def main():
    print("🔍 Verificando usuario vendedor...")
    
    db_path = 'panaderia.db'
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada. Ejecuta primero el script de inicialización.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        cursor = conn.cursor()
        
        # Buscar usuario vendedor
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", ('vendedor@migasdeoro.com',))
        vendedor = cursor.fetchone()
        
        if vendedor:
            print("✅ Usuario vendedor encontrado:")
            print(f"   ID: {vendedor['id']}")
            print(f"   Nombre: {vendedor['nombre']}")
            print(f"   Email: {vendedor['email']}")
            print(f"   Rol: {vendedor['rol']}")
            
            # Verificar contraseña
            password_correcta = verificar_password('vendedor123', vendedor['password'])
            if password_correcta:
                print("✅ Contraseña correcta")
            else:
                print("❌ Contraseña incorrecta, actualizando...")
                # Actualizar contraseña
                new_password_hash = hashlib.sha256('vendedor123'.encode()).hexdigest()
                cursor.execute("UPDATE usuarios SET password = ? WHERE id = ?", 
                             (new_password_hash, vendedor['id']))
                conn.commit()
                print("✅ Contraseña actualizada")
        else:
            print("❌ Usuario vendedor no encontrado, creando...")
            
            # Crear usuario vendedor
            password_hash = hashlib.sha256('vendedor123'.encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                'Vendedor',  # Cambiando "Vendedor Principal" a solo "Vendedor"
                'vendedor@migasdeoro.com',
                password_hash,
                '555-0123',
                'Tienda Principal',
                'vendedor'
            ))
            conn.commit()
            vendedor_id = cursor.lastrowid
            print(f"✅ Usuario vendedor creado con ID: {vendedor_id}")
        
        print("\n📝 Credenciales del vendedor:")
        print("   Email: vendedor@migasdeoro.com")
        print("   Contraseña: vendedor123")
        
        # Verificar que el usuario puede hacer login
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND rol = ?", 
                      ('vendedor@migasdeoro.com', 'vendedor'))
        vendedor_final = cursor.fetchone()
        
        if vendedor_final:
            password_test = verificar_password('vendedor123', vendedor_final['password'])
            if password_test:
                print("✅ Login verificado correctamente")
            else:
                print("❌ Error en verificación de login")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
