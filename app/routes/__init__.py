from flask import Blueprint

def register_blueprints(app):
    """Registra todos los blueprints de la aplicación"""
    from .auth import auth_bp
    from .productos import productos_bp
    from .dashboard import dashboard_bp
    from .ventas import ventas_bp
    from .api import api_bp  # Agregado blueprint API
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(api_bp)  # Registrado blueprint API
    
    @app.route('/')
    def index():
        from flask import render_template
        from app.models.producto import Producto
        productos_destacados = Producto.get_all(limit=6)
        return render_template('productos/index.html', productos=productos_destacados)
    
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
                    # Convertir tuplas de favoritos a objetos producto
                    for favorito in favoritos_data:
                        # favorito[4] = nombre, favorito[5] = precio, favorito[6] = imagen, favorito[7] = descripcion
                        producto_obj = type('Producto', (), {
                            'id': favorito[2],  # producto_id
                            'nombre': favorito[4],
                            'precio': favorito[5],
                            'imagen_url': favorito[6],
                            'descripcion': favorito[7]
                        })()
                        productos_favoritos.append(producto_obj)
            except Exception as e:
                print(f"[v0] Error obteniendo favoritos de BD: {e}")
        else:
            favoritos_ids = session.get('favoritos', [])
            
            if favoritos_ids:
                for producto_id in favoritos_ids:
                    producto = Producto.find_by_id(producto_id)
                    if producto:
                        productos_favoritos.append(producto)
        
        return render_template('favoritos.html', productos=productos_favoritos)
    
    @app.route('/placeholder.svg')
    def placeholder_svg():
        from flask import request, Response
        
        # Obtener parámetros de la URL
        height = request.args.get('height', '200')
        width = request.args.get('width', '300')
        query = request.args.get('query', 'producto')
        
        # Generar SVG dinámico sin texto placeholder
        svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#f3f4f6"/>
            <circle cx="50%" cy="40%" r="20" fill="#d1d5db"/>
            <rect x="30%" y="60%" width="40%" height="8" fill="#d1d5db" rx="4"/>
            <rect x="35%" y="75%" width="30%" height="6" fill="#e5e7eb" rx="3"/>
        </svg>'''
        
        return Response(svg_content, mimetype='image/svg+xml')
