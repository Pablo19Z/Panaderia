from flask import Flask
from config import config
import os

def create_app(config_name=None):
    """Factory function para crear la aplicación Flask"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
    app.config.from_object(config[config_name])
    
    # Crear carpetas necesarias
    os.makedirs('instance', exist_ok=True)
    os.makedirs('app/static', exist_ok=True)
    os.makedirs('app/static/images', exist_ok=True)
    os.makedirs('app/static/images/uploads', exist_ok=True)
    os.makedirs('app/static/images/productos', exist_ok=True)
    
    # Registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Inicializar base de datos
    from app.models import init_db
    with app.app_context():
        init_db()
    
    return app

app = create_app()
