from datetime import datetime
from . import get_db_connection

class Insumo:
    def __init__(self, id=None, nombre=None, descripcion=None, cantidad_actual=0, cantidad_minima=0, unidad_medida='kg', precio_compra=None, proveedor=None, fecha_actualizacion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad_actual = cantidad_actual
        self.cantidad_minima = cantidad_minima
        self.unidad_medida = unidad_medida
        self.precio_compra = precio_compra
        self.proveedor = proveedor
        self.fecha_actualizacion = fecha_actualizacion or datetime.now()
    
    @staticmethod
    def create_table():
        """Crea la tabla de insumos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad_actual DECIMAL(10,2) DEFAULT 0,
                cantidad_minima DECIMAL(10,2) DEFAULT 0,
                unidad_medida TEXT DEFAULT 'kg',
                precio_compra DECIMAL(10,2),
                proveedor TEXT,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo insumo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO insumos (nombre, descripcion, cantidad_actual, cantidad_minima, unidad_medida, precio_compra, proveedor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['nombre'], data.get('descripcion'), data.get('cantidad_actual', 0), 
              data.get('cantidad_minima', 0), data.get('unidad_medida', 'kg'), 
              data.get('precio_compra'), data.get('proveedor')))
        
        insumo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return insumo_id
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los insumos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM insumos ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_low_stock(cls):
        """Obtiene insumos con stock bajo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM insumos WHERE cantidad_actual <= cantidad_minima ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def find_by_id(cls, insumo_id):
        """Busca un insumo por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM insumos WHERE id = ?', (insumo_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    def update_cantidad(self, nueva_cantidad):
        """Actualiza la cantidad del insumo"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE insumos SET cantidad_actual = ?, fecha_actualizacion = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (nueva_cantidad, self.id))
        conn.commit()
        conn.close()
        self.cantidad_actual = nueva_cantidad
        self.fecha_actualizacion = datetime.now()
    
    def is_low_stock(self):
        """Verifica si el insumo tiene stock bajo"""
        return self.cantidad_actual <= self.cantidad_minima
    
    def update(self, data):
        """Actualiza los datos del insumo"""
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
            fields.append("fecha_actualizacion = CURRENT_TIMESTAMP")
            values.append(self.id)
            cursor.execute(f'UPDATE insumos SET {", ".join(fields)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
