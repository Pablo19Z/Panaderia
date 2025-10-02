from flask import Blueprint

def register_blueprints(app):
    """Registra todos los blueprints de la aplicación"""
    from .auth import auth_bp
    from .productos import productos_bp
    from .dashboard import dashboard_bp
    from .ventas import ventas_bp
    from .api import api_bp
    from .reportes import reportes_bp
    from .usuarios import usuarios_bp
    from .clientes import clientes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(clientes_bp)
    
    @app.route('/')
    def index():
        from flask import render_template
        from app.models.producto import Producto
        from app.models.system_settings import SystemSettings
        
        productos_destacados = Producto.get_all(limit=6)
        
        try:
            SystemSettings.create_table()  # Asegurar que la tabla existe
            hero_background_url = SystemSettings.get_setting('hero_background_url') or '/placeholder.svg?height=600&width=1200'
        except:
            hero_background_url = '/placeholder.svg?height=600&width=1200'
        
        return render_template('inicio.html', 
                             productos_destacados=productos_destacados,
                             hero_background_url=hero_background_url)
    
    @app.route('/favoritos')
    def favoritos():
        from flask import render_template, session
        from app.models.producto import Producto
        from app.models.cliente import Cliente
        
        productos_favoritos = []
        
        if 'user_id' in session:
            try:
                cliente = Cliente.find_by_id(session['user_id'])
                if cliente:
                    favoritos_data = cliente.get_favoritos()
                    for favorito in favoritos_data:
                        producto_obj = type('Producto', (), {
                            'id': favorito[2],
                            'nombre': favorito[4],
                            'precio': favorito[5],
                            'imagen_url': favorito[6],
                            'descripcion': favorito[7] if favorito[7] else 'Delicioso producto de nuestra panadería'
                        })()
                        productos_favoritos.append(producto_obj)
            except Exception as e:
                productos_favoritos = []
        else:
            favoritos_ids = session.get('favoritos', [])
            
            if favoritos_ids:
                for producto_id in favoritos_ids:
                    producto = Producto.find_by_id(producto_id)
                    if producto:
                        productos_favoritos.append(producto)
        
        return render_template('favoritos.html', productos=productos_favoritos)
    
    @app.route('/historia')
    def historia():
        from flask import render_template
        from app.models.system_settings import SystemSettings
        from app.models.historia_images import HistoriaImages
        
        try:
            SystemSettings.create_table()
            hero_background_url = SystemSettings.get_setting('hero_background_url') or '/placeholder.svg?height=500&width=1200'
            
            HistoriaImages.create_table()
            historia_images = HistoriaImages.get_all_images()
            
            # Provide default values if not set
            images = {
                'hero_background': historia_images.get('hero_background', {}).get('url', hero_background_url),
                'inicios_image': historia_images.get('inicios_image', {}).get('url', '/placeholder.svg?height=400&width=600'),
                'timeline_1985': historia_images.get('timeline_1985', {}).get('url', '/placeholder.svg?height=150&width=200'),
                'timeline_1995': historia_images.get('timeline_1995', {}).get('url', '/placeholder.svg?height=150&width=200'),
                'timeline_2010': historia_images.get('timeline_2010', {}).get('url', '/placeholder.svg?height=150&width=200'),
                'timeline_2024': historia_images.get('timeline_2024', {}).get('url', '/placeholder.svg?height=150&width=200'),
                'valores_image': historia_images.get('valores_image', {}).get('url', '/placeholder.svg?height=400&width=600')
            }
        except:
            # Fallback to defaults if there's any error
            hero_background_url = '/placeholder.svg?height=500&width=1200'
            images = {
                'hero_background': hero_background_url,
                'inicios_image': '/placeholder.svg?height=400&width=600',
                'timeline_1985': '/placeholder.svg?height=150&width=200',
                'timeline_1995': '/placeholder.svg?height=150&width=200',
                'timeline_2010': '/placeholder.svg?height=150&width=200',
                'timeline_2024': '/placeholder.svg?height=150&width=200',
                'valores_image': '/placeholder.svg?height=400&width=600'
            }
        
        return render_template('historia.html', 
                             hero_background_url=hero_background_url,
                             historia_images=images)
    
    
    @app.route('/placeholder.svg')
    def placeholder_svg():
        from flask import request, Response
        
        height = request.args.get('height', '200')
        width = request.args.get('width', '300')
        query = request.args.get('query', 'producto')
        
        svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#f9fafb;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#f3f4f6;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#bg)" stroke="#e5e7eb" stroke-width="1"/>
            <circle cx="50%" cy="35%" r="25" fill="#d1d5db"/>
            <path d="M{int(width)*0.4} {int(height)*0.5} Q{int(width)*0.5} {int(height)*0.45} {int(width)*0.6} {int(height)*0.5} 
                     L{int(width)*0.65} {int(height)*0.7} L{int(width)*0.35} {int(height)*0.7} Z" fill="#d1d5db"/>
            <rect x="25%" y="75%" width="50%" height="4" fill="#d1d5db" rx="2"/>
            <rect x="30%" y="85%" width="40%" height="3" fill="#e5e7eb" rx="1.5"/>
        </svg>'''
        
        return Response(svg_content, mimetype='image/svg+xml')
