from . import get_db_connection

class DetalleVenta:
    """
    Modelo para los detalles de venta (items individuales de cada pedido).
    
    IMPORTANTE - SEGURIDAD DE PRECIOS:
    El campo 'precio_unitario' almacena el precio del producto AL MOMENTO DE LA VENTA.
    Este precio NUNCA cambia, incluso si el precio del producto se modifica después.
    Esto garantiza que:
    - Las ventas históricas mantienen sus precios originales
    - Los PDFs y reportes siempre muestran el precio correcto
    - Los cambios de precio no afectan cálculos pasados
    - Hay una auditoría completa del historial de precios
    """
    
    def __init__(self, id=None, pedido_id=None, producto_id=None, cantidad=None, precio_unitario=None):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario  # Precio congelado al momento de la venta
    
    @staticmethod
    def create_table():
        """Crea la tabla de detalles de venta"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """
        Crea un nuevo detalle de venta.
        El precio_unitario debe ser el precio actual del producto al momento de la venta.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        ''', (data['pedido_id'], data['producto_id'], data['cantidad'], data['precio_unitario']))
        
        detalle_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return detalle_id
    
    @classmethod
    def create_multiple(cls, detalles):
        """
        Crea múltiples detalles de venta en una sola transacción.
        Cada detalle debe incluir el precio_unitario capturado al momento de la venta.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for detalle in detalles:
            cursor.execute('''
                INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            ''', (detalle['pedido_id'], detalle['producto_id'], detalle['cantidad'], detalle['precio_unitario']))
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_pedido(cls, pedido_id):
        """Obtiene todos los detalles de un pedido"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM detalle_pedidos WHERE pedido_id = ?', (pedido_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    def get_subtotal(self):
        """
        Calcula el subtotal del detalle usando el precio histórico.
        Este cálculo siempre usa precio_unitario (precio al momento de la venta),
        NO el precio actual del producto.
        """
        return self.cantidad * self.precio_unitario
