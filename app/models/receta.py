from datetime import datetime
from . import get_db_connection

class Receta:
    """
    Modelo para recetas de la panadería.
    Permite gestionar recetas con ingredientes, instrucciones y detalles de preparación.
    """
    
    def __init__(self, id=None, nombre=None, descripcion=None, ingredientes=None, 
                 instrucciones=None, tiempo_preparacion=None, porciones=None, 
                 dificultad=None, imagen=None, categoria_id=None, activo=True, fecha_creacion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.ingredientes = ingredientes  # Texto con lista de ingredientes
        self.instrucciones = instrucciones  # Texto con pasos de preparación
        self.tiempo_preparacion = tiempo_preparacion  # En minutos
        self.porciones = porciones  # Número de porciones
        self.dificultad = dificultad  # Fácil, Media, Difícil
        self.imagen = imagen
        self.categoria_id = categoria_id
        self.activo = activo
        self.fecha_creacion = fecha_creacion or datetime.now()
    
    @property
    def imagen_url(self):
        """Retorna la URL de la imagen de la receta"""
        if self.imagen and self.imagen.startswith('http'):
            return self.imagen
        else:
            return f'/placeholder.svg?height=200&width=300'
    
    @staticmethod
    def create_table():
        """Crea la tabla de recetas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                ingredientes TEXT,
                instrucciones TEXT,
                tiempo_preparacion INTEGER,
                porciones INTEGER,
                dificultad TEXT,
                imagen TEXT,
                categoria_id INTEGER,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """Crea una nueva receta"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recetas (nombre, descripcion, ingredientes, instrucciones, 
                               tiempo_preparacion, porciones, dificultad, imagen, categoria_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['nombre'], data.get('descripcion'), data.get('ingredientes'),
              data.get('instrucciones'), data.get('tiempo_preparacion'), 
              data.get('porciones'), data.get('dificultad'), 
              data.get('imagen'), data.get('categoria_id')))
        
        receta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return receta_id
    
    @classmethod
    def get_all(cls, categoria_id=None, limit=None, include_inactive=False):
        """Obtiene todas las recetas, opcionalmente filtradas por categoría"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if include_inactive:
            query = 'SELECT * FROM recetas'
        else:
            query = 'SELECT * FROM recetas WHERE activo = 1'
        
        params = []
        
        if categoria_id:
            if include_inactive:
                query += ' WHERE categoria_id = ?'
            else:
                query += ' AND categoria_id = ?'
            params.append(categoria_id)
        
        query += ' ORDER BY fecha_creacion DESC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def find_by_id(cls, receta_id):
        """Busca una receta por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recetas WHERE id = ? AND activo = 1', (receta_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    @classmethod
    def search(cls, query):
        """Busca recetas por nombre o descripción"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM recetas 
            WHERE (nombre LIKE ? OR descripcion LIKE ?) AND activo = 1
            ORDER BY nombre
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    def update(self, data):
        """Actualiza los datos de la receta"""
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
            cursor.execute(f'UPDATE recetas SET {", ".join(fields)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
