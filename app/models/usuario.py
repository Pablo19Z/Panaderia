import hashlib
from datetime import datetime
from . import get_db_connection

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None, telefono=None, direccion=None, rol='cliente', fecha_registro=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.telefono = telefono
        self.direccion = direccion
        self.rol = rol
        self.fecha_registro = fecha_registro or datetime.now()
        self.activo = activo
    
    @staticmethod
    def create_table():
        """Crea la tabla de usuarios"""
        conn = get_db_connection()
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
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_password(password):
        """Hashea una contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        hashed_password = cls.hash_password(data['password'])
        
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['nombre'], data['email'], hashed_password, 
              data.get('telefono'), data.get('direccion'), data.get('rol', 'cliente')))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    @classmethod
    def find_by_email(cls, email):
        """Busca un usuario por email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND activo = 1', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    @classmethod
    def find_by_id(cls, user_id):
        """Busca un usuario por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ? AND activo = 1', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    @classmethod
    def get_all(cls, role=None):
        """Obtiene todos los usuarios, opcionalmente filtrados por rol"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if role:
            cursor.execute('SELECT * FROM usuarios WHERE rol = ? AND activo = 1 ORDER BY nombre', (role,))
        else:
            cursor.execute('SELECT * FROM usuarios WHERE activo = 1 ORDER BY nombre')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_by_role(cls, role):
        """Obtiene usuarios por rol específico"""
        return cls.get_all(role=role)
    
    @classmethod
    def get_vendedores_top_mes(cls, año, mes):
        """Obtiene los vendedores con mejores ventas del mes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.*, COUNT(p.id) as total_pedidos, COALESCE(SUM(p.total), 0) as total_ventas
            FROM usuarios u
            LEFT JOIN pedidos p ON u.id = p.usuario_id 
                AND strftime('%Y', p.fecha_pedido) = ? 
                AND strftime('%m', p.fecha_pedido) = ?
                AND p.estado != 'cancelado'
            WHERE u.rol = 'vendedor' AND u.activo = 1
            GROUP BY u.id
            ORDER BY total_ventas DESC
            LIMIT 5
        ''', (str(año), f"{mes:02d}"))
        
        rows = cursor.fetchall()
        conn.close()
        
        vendedores = []
        for row in rows:
            vendedor = cls(*row[:9])  # Los primeros 9 campos son del usuario
            vendedor.total_pedidos = row[9]
            vendedor.total_ventas = row[10]
            vendedores.append(vendedor)
        
        return vendedores
    
    @classmethod
    def count(cls):
        """Cuenta el total de usuarios"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE activo = 1')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    @classmethod
    def count_by_role(cls, role):
        """Cuenta usuarios por rol específico"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE rol = ? AND activo = 1', (role,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def verify_password(self, password):
        """Verifica si la contraseña es correcta"""
        return self.password == self.hash_password(password)
    
    def update(self, data):
        """Actualiza los datos del usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if 'password' in data:
            data['password'] = self.hash_password(data['password'])
        
        fields = []
        values = []
        for key, value in data.items():
            if hasattr(self, key):
                fields.append(f"{key} = ?")
                values.append(value)
                setattr(self, key, value)
        
        if fields:
            values.append(self.id)
            cursor.execute(f'UPDATE usuarios SET {", ".join(fields)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
    
    def delete(self):
        """Desactiva el usuario (soft delete)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET activo = 0 WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
        self.activo = False
    
    def save(self):
        """Guarda el usuario en la base de datos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            hashed_password = self.hash_password(self.password)
            
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, password, telefono, direccion, rol)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.nombre, self.email, hashed_password, 
                  self.telefono, self.direccion, self.rol))
            
            self.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[v0] Error guardando usuario: {e}")
            conn.close()
            return False
