import sqlite3
import hashlib
import os

def crear_empleados_directo():
    """Crear usuarios empleados de forma directa en la base de datos"""
    print("🔧 Creando usuarios empleados...")
    
    db_path = 'panaderia.db'
    if not os.path.exists(db_path):
        print("⚠️ Base de datos no encontrada, creando nueva...")
    
    # Conectar directamente a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT,
            rol TEXT DEFAULT 'cliente' CHECK(rol IN ('cliente', 'admin', 'vendedor', 'chef')),
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Hash de las contraseñas
    import hashlib
    chef_password = hashlib.sha256('chef123'.encode()).hexdigest()
    vendedor_password = hashlib.sha256('venta123'.encode()).hexdigest()
    
    empleados = [
        {
            'nombre': 'Carlos Mendoza',
            'email': 'chef@panaderia.com',
            'password': chef_password,
            'rol': 'chef',
            'telefono': '555-0103',
            'activo': 1
        },
        {
            'nombre': 'Ana Rodriguez',
            'email': 'vendedor@panaderia.com', 
            'password': vendedor_password,
            'rol': 'vendedor',
            'telefono': '555-0104',
            'activo': 1
        }
    ]
    
    try:
        for empleado in empleados:
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", (empleado['email'],))
            if cursor.fetchone():
                print(f"✅ Usuario {empleado['email']} ya existe")
                continue
            
            # Insertar nuevo usuario
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, rol, telefono, activo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                empleado['nombre'],
                empleado['email'], 
                empleado['password'],
                empleado['rol'],
                empleado['telefono'],
                empleado['activo']
            ))
            print(f"✅ Usuario {empleado['email']} creado exitosamente")
        
        conn.commit()
        print("\n🎉 Usuarios empleados creados correctamente!")
        print("\n📋 Credenciales de acceso:")
        print("Chef: chef@panaderia.com / chef123")
        print("Vendedor: vendedor@panaderia.com / venta123")
        
    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    crear_empleados_directo()
