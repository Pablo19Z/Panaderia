from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.cliente import Cliente
from app.utils.decorators import login_required

productos_bp = Blueprint('productos', __name__)

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    from app.models.usuario import Usuario
    return Usuario.find_by_id(session['user_id'])

def get_cart_count():
    """Obtiene el número de items en el carrito"""
    if 'user_id' not in session:
        return 0
    cliente = Cliente.find_by_id(session['user_id'])
    return cliente.contar_items_carrito() if cliente else 0

@productos_bp.route('/')
def index():
    """Página principal de la panadería"""
    productos_destacados = Producto.get_all(limit=6)
    categorias = Categoria.get_all()
    
    usuario = get_current_user()
    carrito_count = get_cart_count()
    
    return render_template('productos/index.html', 
                         productos=productos_destacados, 
                         categorias=categorias,
                         usuario=usuario,
                         carrito_count=carrito_count)

@productos_bp.route('/productos')
def catalogo():
    """Página de catálogo de productos"""
    categoria_id = request.args.get('categoria', type=int)
    busqueda = request.args.get('q', '')
    
    if busqueda:
        productos_lista = Producto.search(busqueda)
    else:
        productos_lista = Producto.get_all(categoria_id=categoria_id)
    
    categorias = Categoria.get_all()
    categoria_actual = Categoria.find_by_id(categoria_id) if categoria_id else None
    
    usuario = get_current_user()
    carrito_count = get_cart_count()
    
    return render_template('productos/catalogo.html', 
                         productos=productos_lista,
                         categorias=categorias,
                         categoria_actual=categoria_actual,
                         busqueda=busqueda,
                         usuario=usuario,
                         carrito_count=carrito_count)

@productos_bp.route('/producto/<int:producto_id>')
def detalle(producto_id):
    """Página de detalle de un producto específico"""
    producto = Producto.find_by_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.catalogo'))
    
    productos_relacionados = Producto.get_all(limit=4)
    # Filtrar el producto actual de los relacionados
    productos_relacionados = [p for p in productos_relacionados if p.id != producto_id][:4]
    
    usuario = get_current_user()
    carrito_count = get_cart_count()
    
    return render_template('productos/detalle_producto.html',
                         producto=producto,
                         productos_relacionados=productos_relacionados,
                         usuario=usuario,
                         carrito_count=carrito_count)

# Las rutas de carrito y favoritos ahora están en app/routes/api.py
