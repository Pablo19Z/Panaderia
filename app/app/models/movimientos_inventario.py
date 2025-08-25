from datetime import datetime
from . import get_db_connection

class MovimientoInventario:
    def __init__(self, id=None, insumo_id=None, tipo_movimiento=None, cantidad=None, motivo=None, usuario_id=None, fecha_movimiento=None):
        self.id = id
        self.insumo_id = insumo_id
        self.tipo_movimiento = tipo_movimiento  # 'entrada' o 'salida'
        self.cantidad = cantidad
        self.motivo = motivo
        self.usuario_id = usuario_id
        self.fecha_movimiento = fecha_movimiento or datetime.now()
    
    @staticmethod
    def create_table():
        """Crea la tabla de movimientos de inventario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos_inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insumo_id INTEGER,
                tipo_movimiento TEXT CHECK(tipo_movimiento IN ('entrada', 'salida')),
                cantidad DECIMAL(10,2) NOT NULL,
                motivo TEXT,
                usuario_id INTEGER,
                fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (insumo_id) REFERENCES insumos (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo movimiento de inventario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO movimientos_inventario (insumo_id, tipo_movimiento, cantidad, motivo, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['insumo_id'], data['tipo_movimiento'], data['cantidad'], 
              data.get('motivo'), data.get('usuario_id')))
        
        movimiento_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Actualizar el stock del insumo
        cls._actualizar_stock_insumo(data['insumo_id'], data['tipo_movimiento'], data['cantidad'])
        
        return movimiento_id
    
    @classmethod
    def _actualizar_stock_insumo(cls, insumo_id, tipo_movimiento, cantidad):
        """Actualiza el stock del insumo según el tipo de movimiento"""
        from .insumo import Insumo
        
        insumo = Insumo.find_by_id(insumo_id)
        if insumo:
            if tipo_movimiento == 'entrada':
                nueva_cantidad = insumo.cantidad_actual + cantidad
            else:  # salida
                nueva_cantidad = max(0, insumo.cantidad_actual - cantidad)
            
            insumo.update_cantidad(nueva_cantidad)
    
    @classmethod
    def get_all(cls, insumo_id=None, tipo_movimiento=None, limit=None):
        """Obtiene todos los movimientos, opcionalmente filtrados"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT m.*, i.nombre as insumo_nombre, u.nombre as usuario_nombre
            FROM movimientos_inventario m
            JOIN insumos i ON m.insumo_id = i.id
            LEFT JOIN usuarios u ON m.usuario_id = u.id
        '''
        params = []
        conditions = []
        
        if insumo_id:
            conditions.append('m.insumo_id = ?')
            params.append(insumo_id)
        
        if tipo_movimiento:
            conditions.append('m.tipo_movimiento = ?')
            params.append(tipo_movimiento)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY m.fecha_movimiento DESC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return rows
    
    @classmethod
    def get_resumen_movimientos(cls, fecha_inicio=None, fecha_fin=None):
        """Obtiene un resumen de movimientos por período"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                tipo_movimiento,
                COUNT(*) as total_movimientos,
                SUM(cantidad) as total_cantidad
            FROM movimientos_inventario
        '''
        params = []
        
        if fecha_inicio and fecha_fin:
            query += ' WHERE fecha_movimiento BETWEEN ? AND ?'
            params.extend([fecha_inicio, fecha_fin])
        elif fecha_inicio:
            query += ' WHERE fecha_movimiento >= ?'
            params.append(fecha_inicio)
        elif fecha_fin:
            query += ' WHERE fecha_movimiento <= ?'
            params.append(fecha_fin)
        
        query += ' GROUP BY tipo_movimiento'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return {row[0]: {'movimientos': row[1], 'cantidad': row[2]} for row in rows}
    
    @classmethod
    def registrar_entrada(cls, insumo_id, cantidad, motivo, usuario_id=None):
        """Registra una entrada de inventario"""
        return cls.create({
            'insumo_id': insumo_id,
            'tipo_movimiento': 'entrada',
            'cantidad': cantidad,
            'motivo': motivo,
            'usuario_id': usuario_id
        })
    
    @classmethod
    def registrar_salida(cls, insumo_id, cantidad, motivo, usuario_id=None):
        """Registra una salida de inventario"""
        return cls.create({
            'insumo_id': insumo_id,
            'tipo_movimiento': 'salida',
            'cantidad': cantidad,
            'motivo': motivo,
            'usuario_id': usuario_id
        })
    
    @classmethod
    def get_movimientos_recientes(cls, limit=10):
        """Obtiene los movimientos más recientes"""
        return cls.get_all(limit=limit)
