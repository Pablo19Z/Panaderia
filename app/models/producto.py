from datetime import datetime
from . import get_db_connection

class Producto:
    """
    Modelo para productos del catálogo.
    
    IMPORTANTE - GESTIÓN DE PRECIOS:
    El campo 'precio' representa el precio ACTUAL del producto en el catálogo.
    Puedes cambiar este precio en cualquier momento sin afectar:
    - Ventas históricas (usan precio_unitario en detalle_pedidos)
    - PDFs de pedidos anteriores
    - Reportes y estadísticas pasadas
    
    Cuando se realiza una venta, el precio actual se COPIA a detalle_pedidos.precio_unitario
    y queda congelado permanentemente para ese pedido específico.
    """
    
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, categoria_id=None, stock=0, imagen=None, activo=True, fecha_creacion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio  # Precio actual en el catálogo (puede cambiar)
        self.categoria_id = categoria_id
        self.stock = stock
        self.imagen = imagen
        self.activo = activo
        self.fecha_creacion = fecha_creacion or datetime.now()
    
    @property
    def imagen_url(self):
        """Retorna la URL de la imagen del producto"""
        if self.imagen and self.imagen.startswith('http'):
            return self.imagen
        else:
            # Generate placeholder with product name for better visual identification
            return f'/placeholder.svg?height=200&width=300'
    
    @staticmethod
    def create_table():
        """Crea la tabla de productos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio DECIMAL(10,2) NOT NULL,
                categoria_id INTEGER,
                stock INTEGER DEFAULT 0,
                imagen TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')
        
        # Tablas relacionadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrito (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER DEFAULT 1,
                fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favoritos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                producto_id INTEGER,
                fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                UNIQUE(usuario_id, producto_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resenas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                producto_id INTEGER,
                calificacion INTEGER CHECK(calificacion >= 1 AND calificacion <= 5),
                comentario TEXT,
                fecha_resena TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes_chat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                mensaje TEXT NOT NULL,
                respuesta TEXT,
                fecha_mensaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, categoria_id, stock, imagen)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['nombre'], data.get('descripcion'), data['precio'], 
              data.get('categoria_id'), data.get('stock', 0), data.get('imagen')))
        
        producto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return producto_id
    
    @classmethod
    def get_all(cls, categoria_id=None, limit=None):
        """Obtiene todos los productos, opcionalmente filtrados por categoría"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM productos WHERE activo = 1'
        params = []
        
        if categoria_id:
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
    def find_by_id(cls, producto_id):
        """Busca un producto por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ? AND activo = 1', (producto_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    @classmethod
    def search(cls, query):
        """Busca productos por nombre o descripción"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM productos 
            WHERE (nombre LIKE ? OR descripcion LIKE ?) AND activo = 1
            ORDER BY nombre
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_mas_vendidos_mes(cls, año, mes):
        """Obtiene los productos más vendidos del mes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, COALESCE(SUM(dp.cantidad), 0) as total_vendido
            FROM productos p
            LEFT JOIN detalle_pedidos dp ON p.id = dp.producto_id
            LEFT JOIN pedidos pe ON dp.pedido_id = pe.id
                AND strftime('%Y', pe.fecha_pedido) = ? 
                AND strftime('%m', pe.fecha_pedido) = ?
                AND pe.estado != 'cancelado'
            WHERE p.activo = 1
            GROUP BY p.id
            ORDER BY total_vendido DESC
            LIMIT 10
        ''', (str(año), f"{mes:02d}"))
        
        rows = cursor.fetchall()
        conn.close()
        
        productos = []
        for row in rows:
            producto = cls(*row[:9])  # Los primeros 9 campos son del producto
            producto.total_vendido = row[9]
            productos.append(producto)
        
        return productos
    
    def get_reviews(self):
        """Obtiene las reseñas del producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, u.nombre as usuario_nombre
            FROM resenas r
            JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.producto_id = ?
            ORDER BY r.fecha_resena DESC
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_average_rating(self):
        """Obtiene la calificación promedio del producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT AVG(calificacion) FROM resenas WHERE producto_id = ?', (self.id,))
        result = cursor.fetchone()[0]
        conn.close()
        return round(result, 1) if result else 0
    
    def update_stock(self, cantidad):
        """Actualiza el stock del producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET stock = stock + ? WHERE id = ?', (cantidad, self.id))
        conn.commit()
        conn.close()
        self.stock += cantidad
    
    def update(self, data):
        """
        Actualiza los datos del producto, incluyendo el precio.
        
        SEGURO PARA CAMBIOS DE PRECIO:
        Cambiar el precio aquí solo afecta a NUEVAS ventas.
        Las ventas anteriores mantienen sus precios originales en detalle_pedidos.precio_unitario.
        """
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
            cursor.execute(f'UPDATE productos SET {", ".join(fields)} WHERE id = ?', values)
            conn.commit()
        
        conn.close()
