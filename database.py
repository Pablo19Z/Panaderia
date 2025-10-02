import sqlite3
import hashlib
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='panaderia.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Inicializa la base de datos con todas las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios con roles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                telefono TEXT,
                direccion TEXT,
                rol TEXT DEFAULT 'cliente' CHECK(rol IN ('cliente', 'admin', 'vendedor', 'cocinero', 'chef')),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de productos
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
        
        # Tabla de carrito
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
        
        # Tabla de favoritos
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
        
        # Tabla de pedidos
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
                fecha_entrega DATE,
                hora_entrega TIME,
                comprobante_pago TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabla de detalles de pedidos
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
        
        # Tabla de insumos/inventario
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
        
        # Tabla de reseñas
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
        
        # Tabla de mensajes del chatbot
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
        self.seed_initial_data(cursor)
        conn.close()
    
    def seed_initial_data(self, cursor):
        """Inserta datos iniciales en la base de datos"""
        
        # Verificar si ya existen datos
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] > 0:
            return
        
        # Crear usuario administrador por defecto
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (?, ?, ?, ?)
        ''', ("Administrador", "admin@migasdeoro.com", admin_password, "admin"))
        
        vendedor_password = hashlib.sha256("vendedor123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password, rol, telefono, direccion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("Vendedor", "vendedor@migasdeoro.com", vendedor_password, "vendedor", "555-0123", "Tienda Principal"))
        
        # Crear categorías iniciales
        categorias = [
            ("Panes", "Variedad de panes frescos"),
            ("Pasteles", "Pasteles y tortas para ocasiones especiales"),
            ("Galletas", "Galletas artesanales"),
            ("Bebidas", "Bebidas calientes y frías"),
            ("Desayunos", "Opciones para el desayuno")
        ]
        
        cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)", categorias[0])
        cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)", categorias[1])
        cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)", categorias[2])
        cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)", categorias[3])
        cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)", categorias[4])
        
        # Crear productos iniciales con precios en pesos colombianos
        productos = [
            ("Pan Francés", "Pan francés tradicional recién horneado", 2500.00, 1, 50),
            ("Croissant", "Croissant de mantequilla artesanal", 3500.00, 1, 30),
            ("Torta de Chocolate", "Deliciosa torta de chocolate con cobertura", 32000.00, 2, 10),
            ("Galletas de Avena", "Galletas caseras de avena con pasas", 1500.00, 3, 40),
            ("Café Americano", "Café americano recién preparado", 2800.00, 4, 100),
            ("Sandwich de Jamón", "Sandwich de jamón y queso en pan artesanal", 8500.00, 5, 25)
        ]
        
        for producto in productos:
            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, precio, categoria_id, stock)
                VALUES (?, ?, ?, ?, ?)
            ''', producto)
        
        # Crear insumos iniciales
        insumos = [
            ("Harina de Trigo", "Harina de trigo para panificación", 50.0, 10.0, "kg", 1.20, "Molinos del Sur"),
            ("Azúcar", "Azúcar blanca refinada", 25.0, 5.0, "kg", 0.80, "Azucarera Nacional"),
            ("Mantequilla", "Mantequilla sin sal para repostería", 10.0, 2.0, "kg", 4.50, "Lácteos Premium"),
            ("Huevos", "Huevos frescos de granja", 200.0, 50.0, "unidades", 0.15, "Granja San José"),
            ("Levadura", "Levadura fresca para pan", 5.0, 1.0, "kg", 3.00, "Levaduras Industriales")
        ]
        
        for insumo in insumos:
            cursor.execute('''
                INSERT INTO insumos (nombre, descripcion, cantidad_actual, cantidad_minima, unidad_medida, precio_compra, proveedor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', insumo)

# Instancia global de la base de datos
db = Database()

def get_db_connection():
    """Obtiene una conexión a la base de datos SQLite"""
    return db.get_connection()
