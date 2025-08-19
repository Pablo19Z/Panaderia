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
                    for favorito in favoritos_data:
                        # favorito structure: (f.id, f.usuario_id, f.producto_id, f.fecha_agregado, p.nombre, p.precio, p.imagen, p.descripcion)
                        producto_obj = type('Producto', (), {
                            'id': favorito[2],  # producto_id
                            'nombre': favorito[4],  # p.nombre
                            'precio': favorito[5],  # p.precio
                            'imagen_url': favorito[6],  # p.imagen
                            'descripcion': favorito[7] if favorito[7] else 'Delicioso producto de nuestra panadería'  # p.descripcion
                        })()
                        productos_favoritos.append(producto_obj)
            except Exception as e:
                print(f"[v0] Error obteniendo favoritos de BD: {e}")
                productos_favoritos = []
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
