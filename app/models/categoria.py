from datetime import datetime
from . import get_db_connection

class Categoria:
    def __init__(self, id=None, nombre=None, descripcion=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = activo
    
    @staticmethod
    def create_table():
        """Crea la tabla de categorías"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """Crea una nueva categoría"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO categorias (nombre, descripcion)
            VALUES (?, ?)
        ''', (data['nombre'], data.get('descripcion')))
        
        categoria_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return categoria_id
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las categorías activas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categorias WHERE activo = 1 ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def find_by_id(cls, categoria_id):
        """Busca una categoría por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categorias WHERE id = ? AND activo = 1', (categoria_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    def update(self, data):
        """Actualiza los datos de la categoría"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        fields = []
        values = []
        for key, value in data.items():
            if hasattr(self, key):
                fields.append(f"{key} = ?")
                values.append(value)
                setattr(self, key, value)
        
        if fields:
            values.append(self.id)
            cursor.execute(f'UPDATE categorias SET {", ".join(fields)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
    
    def delete(self):
        """Desactiva la categoría (soft delete)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE categorias SET activo = 0 WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
        self.activo = False
