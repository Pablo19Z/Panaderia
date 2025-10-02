import sqlite3
import os

def verificar_usuarios():
    """Verifica qué usuarios están en la base de datos"""
    
    # Buscar la base de datos en diferentes ubicaciones
    db_paths = [
        'instance/panaderia.db',
        'panaderia.db',
        os.path.join('instance', 'panaderia.db')
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ No se encontró la base de datos en ninguna ubicación")
        print("Ubicaciones buscadas:")
        for path in db_paths:
            print(f"   - {path}")
        return
    
    print(f"✅ Base de datos encontrada en: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si existe la tabla usuarios
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            print("❌ La tabla 'usuarios' no existe")
            conn.close()
            return
        
        # Obtener todos los usuarios
        cursor.execute("SELECT id, nombre, email, rol, activo FROM usuarios")
        usuarios = cursor.fetchall()
        
        print(f"\n📊 Total de usuarios en la base de datos: {len(usuarios)}")
        print("=" * 60)
        
        if usuarios:
            for usuario in usuarios:
                id_user, nombre, email, rol, activo = usuario
                estado = "✅ Activo" if activo else "❌ Inactivo"
                print(f"ID: {id_user}")
                print(f"Nombre: {nombre}")
                print(f"Email: {email}")
                print(f"Rol: {rol}")
                print(f"Estado: {estado}")
                print("-" * 40)
        else:
            print("❌ No hay usuarios en la base de datos")
        
        # Buscar específicamente el usuario vendedor
        cursor.execute("SELECT * FROM usuarios WHERE email = 'vendedor@migasdeoro.com'")
        vendedor = cursor.fetchone()
        
        print("\n🔍 Búsqueda específica del vendedor:")
        if vendedor:
            print("✅ Usuario vendedor encontrado:")
            print(f"   ID: {vendedor[0]}")
            print(f"   Nombre: {vendedor[1]}")
            print(f"   Email: {vendedor[2]}")
            print(f"   Rol: {vendedor[6]}")
            print(f"   Activo: {vendedor[8]}")
        else:
            print("❌ Usuario vendedor NO encontrado")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al acceder a la base de datos: {e}")

if __name__ == "__main__":
    print("🔍 VERIFICANDO USUARIOS EN LA BASE DE DATOS")
    print("=" * 50)
    verificar_usuarios()
