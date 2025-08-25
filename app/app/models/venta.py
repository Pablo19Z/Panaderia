from datetime import datetime
from . import get_db_connection

class Venta:
    def __init__(self, id=None, usuario_id=None, total=None, estado='pendiente', fecha_pedido=None, direccion_entrega=None, telefono_contacto=None, notas=None):
        self.id = id
        self.usuario_id = usuario_id
        self.total = total
        self.estado = estado
        self.fecha_pedido = fecha_pedido or datetime.now()
        self.direccion_entrega = direccion_entrega
        self.telefono_contacto = telefono_contacto
        self.notas = notas
    
    @staticmethod
    def create_table():
        """Crea la tabla de ventas/pedidos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                total DECIMAL(10,2) NOT NULL,
                estado TEXT DEFAULT 'pendiente' CHECK(estado IN ('pendiente', 'preparando', 'listo', 'entregado', 'cancelado')),
                fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                direccion_entrega TEXT,
                telefono_contacto TEXT,
                notas TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """Crea una nueva venta/pedido"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pedidos (usuario_id, total, direccion_entrega, telefono_contacto, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['usuario_id'], data['total'], data.get('direccion_entrega'), 
              data.get('telefono_contacto'), data.get('notas')))
        
        venta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return venta_id
    
    @classmethod
    def get_all(cls, estado=None, usuario_id=None):
        """Obtiene todas las ventas, opcionalmente filtradas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM pedidos'
        params = []
        conditions = []
        
        if estado:
            conditions.append('estado = ?')
            params.append(estado)
        
        if usuario_id:
            conditions.append('usuario_id = ?')
            params.append(usuario_id)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY fecha_pedido DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def find_by_id(cls, venta_id):
        """Busca una venta por ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pedidos WHERE id = ?', (venta_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row)
        return None
    
    def get_detalles(self):
        """Obtiene los detalles de la venta"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT dp.*, p.nombre as producto_nombre
            FROM detalle_pedidos dp
            JOIN productos p ON dp.producto_id = p.id
            WHERE dp.pedido_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def update_estado(self, nuevo_estado):
        """Actualiza el estado de la venta"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE pedidos SET estado = ? WHERE id = ?', (nuevo_estado, self.id))
        conn.commit()
        conn.close()
        self.estado = nuevo_estado
    
    @classmethod
    def get_estadisticas(cls):
        """Obtiene estadísticas de ventas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de ventas del día
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total), 0)
            FROM pedidos 
            WHERE DATE(fecha_pedido) = DATE('now')
        ''')
        ventas_hoy = cursor.fetchone()
        
        # Total de ventas del mes
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total), 0)
            FROM pedidos 
            WHERE strftime('%Y-%m', fecha_pedido) = strftime('%Y-%m', 'now')
        ''')
        ventas_mes = cursor.fetchone()
        
        # Pedidos por estado
        cursor.execute('''
            SELECT estado, COUNT(*)
            FROM pedidos
            GROUP BY estado
        ''')
        pedidos_por_estado = cursor.fetchall()
        
        conn.close()
        
        return {
            'ventas_hoy': {'cantidad': ventas_hoy[0], 'total': ventas_hoy[1]},
            'ventas_mes': {'cantidad': ventas_mes[0], 'total': ventas_mes[1]},
            'pedidos_por_estado': dict(pedidos_por_estado)
        }
