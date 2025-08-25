import sqlite3
from datetime import datetime, date
from app.database import get_db_connection

class Vendedor:
    def __init__(self, id=None, usuario_id=None, zona_asignada=None, meta_mensual=None, 
                 comision_porcentaje=None, ventas_realizadas=0, fecha_contratacion=None, activo=1):
        self.id = id
        self.usuario_id = usuario_id
        self.zona_asignada = zona_asignada
        self.meta_mensual = meta_mensual
        self.comision_porcentaje = comision_porcentaje
        self.ventas_realizadas = ventas_realizadas
        self.fecha_contratacion = fecha_contratacion
        self.activo = activo

    @staticmethod
    def create_table():
        """Crear tabla de vendedores"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                zona_asignada TEXT NOT NULL,
                meta_mensual DECIMAL(10,2) DEFAULT 0,
                comision_porcentaje DECIMAL(5,2) DEFAULT 5.0,
                ventas_realizadas INTEGER DEFAULT 0,
                fecha_contratacion DATE DEFAULT CURRENT_DATE,
                activo INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def create(data):
        """Crear nuevo vendedor"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vendedores (usuario_id, zona_asignada, meta_mensual, comision_porcentaje, fecha_contratacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['usuario_id'],
            data['zona_asignada'],
            data.get('meta_mensual', 0),
            data.get('comision_porcentaje', 5.0),
            data.get('fecha_contratacion', date.today())
        ))
        vendedor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vendedor_id

    @staticmethod
    def find_by_usuario_id(usuario_id):
        """Buscar vendedor por ID de usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendedores WHERE usuario_id = ? AND activo = 1', (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Vendedor(*row)
        return None

    @staticmethod
    def get_all():
        """Obtener todos los vendedores activos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendedores WHERE activo = 1 ORDER BY fecha_contratacion DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [Vendedor(*row) for row in rows]

    def get_estadisticas_ventas(self):
        """Obtener estadísticas de ventas del vendedor"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ventas del día
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total), 0) 
            FROM ventas 
            WHERE vendedor_id = ? AND DATE(fecha_venta) = DATE('now')
        ''', (self.usuario_id,))
        ventas_hoy = cursor.fetchone()
        
        # Ventas del mes
        cursor.execute('''
            SELECT COUNT(*), COALESCE(SUM(total), 0) 
            FROM ventas 
            WHERE vendedor_id = ? AND strftime('%Y-%m', fecha_venta) = strftime('%Y-%m', 'now')
        ''', (self.usuario_id,))
        ventas_mes = cursor.fetchone()
        
        # Productos más vendidos
        cursor.execute('''
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            JOIN ventas v ON dv.venta_id = v.id
            WHERE v.vendedor_id = ?
            GROUP BY p.id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT 5
        ''', (self.usuario_id,))
        productos_top = cursor.fetchall()
        
        conn.close()
        
        # Calcular progreso de meta
        progreso_meta = 0
        if self.meta_mensual > 0:
            progreso_meta = (ventas_mes[1] / self.meta_mensual) * 100
        
        return {
            'ventas_hoy': {'cantidad': ventas_hoy[0], 'total': ventas_hoy[1]},
            'ventas_mes': {'cantidad': ventas_mes[0], 'total': ventas_mes[1]},
            'progreso_meta': min(progreso_meta, 100),
            'productos_top': productos_top,
            'comision_mes': (ventas_mes[1] * self.comision_porcentaje / 100)
        }

    def update(self, data):
        """Actualizar información del vendedor"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE vendedores 
            SET zona_asignada = ?, meta_mensual = ?, comision_porcentaje = ?, 
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('zona_asignada', self.zona_asignada),
            data.get('meta_mensual', self.meta_mensual),
            data.get('comision_porcentaje', self.comision_porcentaje),
            self.id
        ))
        conn.commit()
        conn.close()
