from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///panaderia.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'tu_clave_secreta_aqui'  # Cambia por una clave segura

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Importa los modelos
    from .models import Usuario, Rol, Cliente, Producto, Categoria, ClienteProducto

    # Registra las rutas dinámicamente
    with app.app_context():
        from .routes import register_routes
        register_routes(app)  # Pasa app como argumento

        db.create_all()

        # Datos iniciales de roles
        if not Rol.query.first():
            db.session.add(Rol(nombre='administrador'))
            db.session.add(Rol(nombre='vendedor'))
            db.session.add(Rol(nombre='inventarista'))
            db.session.commit()

        # Datos iniciales de usuarios
        if not Usuario.query.first():
            fecha = datetime.date(2025, 7, 1)
            admin = Usuario(
                nombre='Admin',
                correo='admin@panaderia.com',
                contraseña='admin123',
                rol_id=1,
                cargo='Gerente',
                salario=5000.00,
                fecha_ingreso=fecha
            )
            vendedor = Usuario(
                nombre='Vendedor1',
                correo='vendedor@panaderia.com',
                contraseña='vendedor123',
                rol_id=2,
                cargo='Vendedor',
                salario=3000.00,
                fecha_ingreso=fecha
            )
            inventarista = Usuario(
                nombre='Inventarista1',
                correo='inventarista@panaderia.com',
                contraseña='inventarista123',
                rol_id=3,
                cargo='Inventarista',
                salario=3500.00,
                fecha_ingreso=fecha
            )
            db.session.add_all([admin, vendedor, inventarista])
            db.session.commit()

        # Datos iniciales de categorías
        if not Categoria.query.first():
            categorias = [
                Categoria(nombre='Pasteles', descripcion='Deliciosos pasteles para toda ocasión'),
                Categoria(nombre='Panes', descripcion='Panes frescos y artesanales'),
                Categoria(nombre='Galletas', descripcion='Galletas caseras y crujientes')
            ]
            db.session.add_all(categorias)
            db.session.commit()

        # Datos iniciales de productos
        if not Producto.query.first():
            productos = [
                Producto(
                    nombre='Pastel de Chocolate',
                    descripcion='Pastel esponjoso con cobertura de chocolate',
                    precio_min=25.00,
                    precio_max=35.00,
                    categoria_id=1,
                    imagen='/static/images/pastel_chocolate.jpg',
                    stock=10
                ),
                Producto(
                    nombre='Pan Integral',
                    descripcion='Pan fresco y saludable',
                    precio_min=2.50,
                    precio_max=2.50,
                    categoria_id=2,
                    imagen='/static/images/pan_integral.jpg',
                    stock=50
                ),
                Producto(
                    nombre='Galletas de Avena',
                    descripcion='Galletas crujientes con avena y pasas',
                    precio_min=1.00,
                    precio_max=1.50,
                    categoria_id=3,
                    imagen='/static/images/galletas_avena.jpg',
                    stock=100
                )
            ]
            db.session.add_all(productos)
            db.session.commit()

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import Usuario
    return Usuario.query.get(int(user_id))
