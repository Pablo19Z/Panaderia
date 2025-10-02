from datetime import datetime
from . import get_db_connection

class Venta:
    def __init__(self, id=None, usuario_id=None, total=None, estado='pendiente', fecha_pedido=None, direccion_entrega=None, telefono_contacto=None, notas=None, metodo_pago='efectivo', fecha_entrega=None, hora_entrega=None, comprobante_pago=None):
        self.id = id
        self.usuario_id = usuario_id
        self.total = total
        self.estado = estado
        if isinstance(fecha_pedido, str):
            try:
                self.fecha_pedido = datetime.strptime(fecha_pedido, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    self.fecha_pedido = datetime.strptime(fecha_pedido, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    self.fecha_pedido = datetime.now()
        else:
            self.fecha_pedido = fecha_pedido or datetime.now()
        self.direccion_entrega = direccion_entrega
        self.telefono_contacto = telefono_contacto
        self.notas = notas
        self.metodo_pago = metodo_pago
        self.fecha_entrega = fecha_entrega
        self.hora_entrega = hora_entrega
        self.comprobante_pago = comprobante_pago
    
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
                metodo_pago TEXT DEFAULT 'efectivo',
                fecha_entrega TEXT,
                hora_entrega TEXT,
                comprobante_pago TEXT,
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
            INSERT INTO pedidos (usuario_id, total, direccion_entrega, telefono_contacto, notas, metodo_pago, fecha_entrega, hora_entrega, comprobante_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['usuario_id'], data['total'], data.get('direccion_entrega'), 
              data.get('telefono_contacto'), data.get('notas'), data.get('metodo_pago', 'efectivo'),
              data.get('fecha_entrega'), data.get('hora_entrega'), data.get('comprobante_pago')))
        
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
    
    @classmethod
    def get_ventas_by_vendedor_mes(cls, vendedor_id, año, mes):
        """Obtiene las ventas de un vendedor específico en un mes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.* FROM pedidos p
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE strftime('%Y', p.fecha_pedido) = ? 
            AND strftime('%m', p.fecha_pedido) = ?
            AND p.estado != 'cancelado'
            ORDER BY p.fecha_pedido DESC
        ''', (str(año), f"{mes:02d}"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_pedidos_preparados_by_chef_mes(cls, chef_id, año, mes):
        """Obtiene los pedidos preparados por un chef en un mes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM pedidos 
            WHERE strftime('%Y', fecha_pedido) = ? 
            AND strftime('%m', fecha_pedido) = ?
            AND estado IN ('listo', 'entregado')
            ORDER BY fecha_pedido DESC
        ''', (str(año), f"{mes:02d}"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_ventas_diarias_mes(cls, año, mes):
        """Obtiene las ventas agrupadas por día del mes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(fecha_pedido) as fecha, COUNT(*) as pedidos, SUM(total) as total
            FROM pedidos 
            WHERE strftime('%Y', fecha_pedido) = ? 
            AND strftime('%m', fecha_pedido) = ?
            AND estado != 'cancelado'
            GROUP BY DATE(fecha_pedido)
            ORDER BY fecha
        ''', (str(año), f"{mes:02d}"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{'fecha': row[0], 'pedidos': row[1], 'total': row[2]} for row in rows]
    
    @classmethod
    def get_pedidos_nequi(cls):
        """Obtiene todos los pedidos con método de pago Nequi"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, u.nombre as cliente_nombre, u.email as cliente_email
            FROM pedidos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.metodo_pago = 'nequi'
            ORDER BY p.fecha_pedido DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def update_comprobante(self, comprobante_path):
        """Actualiza el comprobante de pago"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE pedidos SET comprobante_pago = ? WHERE id = ?', (comprobante_path, self.id))
        conn.commit()
        conn.close()
