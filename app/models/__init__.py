import sqlite3
import os
from instance.config import InstanceConfig

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    return sqlite3.connect(InstanceConfig.DATABASE_PATH)

def init_db():
    """Inicializa la base de datos con todas las tablas"""
    from .usuario import Usuario
    from .categoria import Categoria
    from .producto import Producto
    from .venta import Venta
    from .detalle_venta import DetalleVenta
    from .insumo import Insumo
    from .roles import Roles
    from .cliente import Cliente
    from .movimientos_inventario import MovimientoInventario
    from .system_settings import SystemSettings
    from .historia_images import HistoriaImages
    
    # Crear todas las tablas
    Usuario.create_table()
    Categoria.create_table()
    Producto.create_table()
    Venta.create_table()
    DetalleVenta.create_table()
    Insumo.create_table()
    Roles.create_table()
    Cliente.create_table()
    MovimientoInventario.create_table()
    SystemSettings.create_table()
    HistoriaImages.create_table()
    
    # Insertar datos iniciales
    _seed_initial_data()

def _seed_initial_data():
    """Inserta datos iniciales en la base de datos"""
    from .usuario import Usuario
    from .categoria import Categoria
    from .producto import Producto
    from .insumo import Insumo
    
    # Crear usuario administrador si no existe
    if not Usuario.find_by_email('admin@migasdeoro.com'):
        Usuario.create({
            'nombre': 'Administrador',
            'email': 'admin@migasdeoro.com',
            'password': 'admin123',
            'rol': 'admin'
        })
    
    # Crear usuario vendedor si no existe
    if not Usuario.find_by_email('vendedor@migasdeoro.com'):
        Usuario.create({
            'nombre': 'Vendedor',
            'email': 'vendedor@migasdeoro.com',
            'password': 'vendedor123',
            'telefono': '555-0123',
            'direccion': 'Tienda Principal',
            'rol': 'vendedor'
        })
    
    # Crear usuario cliente de prueba si no existe
    if not Usuario.find_by_email('cliente@test.com'):
        Usuario.create({
            'nombre': 'Cliente Test',
            'email': 'cliente@test.com',
            'password': 'cliente123',
            'telefono': '555-0456',
            'direccion': 'Dirección de prueba',
            'rol': 'cliente'
        })
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM categorias')
    categoria_count = cursor.fetchone()[0]
    
    if categoria_count == 0:
        # Crear categorías iniciales
        categorias = [
            {"nombre": "Panes", "descripcion": "Variedad de panes frescos"},
            {"nombre": "Pasteles", "descripcion": "Pasteles y tortas para ocasiones especiales"},
            {"nombre": "Galletas", "descripcion": "Galletas artesanales"},
            {"nombre": "Bebidas", "descripcion": "Bebidas calientes y frías"},
            {"nombre": "Desayunos", "descripcion": "Opciones para el desayuno"}
        ]
        
        for categoria in categorias:
            Categoria.create(categoria)
    
    cursor.execute('SELECT COUNT(*) FROM productos')
    producto_count = cursor.fetchone()[0]
    
    if producto_count == 0:
        # Crear productos iniciales
        productos = [
            {"nombre": "Pan Francés", "descripcion": "Pan francés tradicional recién horneado", "precio": 2.50, "categoria_id": 1, "stock": 50},
            {"nombre": "Croissant", "descripcion": "Croissant de mantequilla artesanal", "precio": 3.00, "categoria_id": 1, "stock": 30},
            {"nombre": "Torta de Chocolate", "descripcion": "Deliciosa torta de chocolate con cobertura", "precio": 25.00, "categoria_id": 2, "stock": 10},
            {"nombre": "Galletas de Avena", "descripcion": "Galletas caseras de avena con pasas", "precio": 1.50, "categoria_id": 3, "stock": 40},
            {"nombre": "Café Americano", "descripcion": "Café americano recién preparado", "precio": 2.00, "categoria_id": 4, "stock": 100},
            {"nombre": "Sandwich de Jamón", "descripcion": "Sandwich de jamón y queso en pan artesanal", "precio": 5.50, "categoria_id": 5, "stock": 25}
        ]
        
        for producto in productos:
            Producto.create(producto)
    
    cursor.execute('SELECT COUNT(*) FROM insumos')
    insumo_count = cursor.fetchone()[0]
    
    if insumo_count == 0:
        # Crear insumos iniciales
        insumos = [
            {"nombre": "Harina de Trigo", "descripcion": "Harina de trigo para panificación", "cantidad_actual": 50.0, "cantidad_minima": 10.0, "unidad_medida": "kg", "precio_compra": 1.20, "proveedor": "Molinos del Sur"},
            {"nombre": "Azúcar", "descripcion": "Azúcar blanca refinada", "cantidad_actual": 25.0, "cantidad_minima": 5.0, "unidad_medida": "kg", "precio_compra": 0.80, "proveedor": "Azucarera Nacional"},
            {"nombre": "Mantequilla", "descripcion": "Mantequilla sin sal para repostería", "cantidad_actual": 10.0, "cantidad_minima": 2.0, "unidad_medida": "kg", "precio_compra": 4.50, "proveedor": "Lácteos Premium"},
            {"nombre": "Huevos", "descripcion": "Huevos frescos de granja", "cantidad_actual": 200.0, "cantidad_minima": 50.0, "unidad_medida": "unidades", "precio_compra": 0.15, "proveedor": "Granja San José"},
            {"nombre": "Levadura", "descripcion": "Levadura fresca para pan", "cantidad_actual": 5.0, "cantidad_minima": 1.0, "unidad_medida": "kg", "precio_compra": 3.00, "proveedor": "Levaduras Industriales"}
        ]
        
        for insumo in insumos:
            Insumo.create(insumo)
    
    conn.close()
