import sqlite3
from datetime import datetime, date
from app.database import get_db_connection

class Chef:
    def __init__(self, id=None, usuario_id=None, especialidad=None, experiencia_anos=None, 
                 certificaciones=None, salario=None, fecha_contratacion=None, activo=1):
        self.id = id
        self.usuario_id = usuario_id
        self.especialidad = especialidad
        self.experiencia_anos = experiencia_anos
        self.certificaciones = certificaciones
        self.salario = salario
        self.fecha_contratacion = fecha_contratacion
        self.activo = activo

    @staticmethod
    def create_table():
        """Crear tabla de chefs"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                especialidad TEXT NOT NULL,
                experiencia_anos INTEGER DEFAULT 0,
                certificaciones TEXT,
                salario DECIMAL(10,2),
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
        """Crear nuevo chef"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chefs (usuario_id, especialidad, experiencia_anos, certificaciones, salario, fecha_contratacion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['usuario_id'],
            data['especialidad'],
            data.get('experiencia_anos', 0),
            data.get('certificaciones', ''),
            data.get('salario', 0),
            data.get('fecha_contratacion', date.today())
        ))
        chef_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return chef_id

    @staticmethod
    def find_by_usuario_id(usuario_id):
        """Buscar chef por ID de usuario"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chefs WHERE usuario_id = ? AND activo = 1', (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Chef(*row)
        return None

    @staticmethod
    def get_all():
        """Obtener todos los chefs activos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chefs WHERE activo = 1 ORDER BY fecha_contratacion DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [Chef(*row) for row in rows]

    def get_estadisticas_produccion(self):
        """Obtener estadísticas de producción del chef"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Productos supervisados hoy
        cursor.execute('''
            SELECT COUNT(*) FROM productos 
            WHERE DATE(created_at) = DATE('now')
        ''')
        productos_hoy = cursor.fetchone()[0]
        
        # Insumos gestionados
        cursor.execute('SELECT COUNT(*) FROM insumos WHERE activo = 1')
        insumos_total = cursor.fetchone()[0]
        
        # Alertas de stock bajo
        cursor.execute('SELECT COUNT(*) FROM insumos WHERE stock_actual <= stock_minimo AND activo = 1')
        alertas_stock = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'productos_hoy': productos_hoy,
            'insumos_total': insumos_total,
            'alertas_stock': alertas_stock,
            'experiencia_anos': self.experiencia_anos
        }

    def update(self, data):
        """Actualizar información del chef"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE chefs 
            SET especialidad = ?, experiencia_anos = ?, certificaciones = ?, 
                salario = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('especialidad', self.especialidad),
            data.get('experiencia_anos', self.experiencia_anos),
            data.get('certificaciones', self.certificaciones),
            data.get('salario', self.salario),
            self.id
        ))
        conn.commit()
        conn.close()
