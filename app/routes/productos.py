from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.cliente import Cliente
from app.models.favorito import Favorito
from app.utils.decorators import login_required, admin_or_vendedor_required

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

def get_user_favorites():
    """Obtiene la lista de IDs de productos favoritos del usuario actual"""
    if 'user_id' in session:
        # Usuario logueado - obtener de base de datos
        user_id = session['user_id']
        cliente = Cliente.find_by_id(user_id)
        if cliente:
            favoritos = cliente.get_favoritos()
            return [str(fav[2]) for fav in favoritos]  # fav[2] es producto_id
    else:
        # Usuario no logueado - obtener de sesión
        return session.get('favoritos', [])
    return []

# @productos_bp.route('/')
# def index():
#     """Página principal de la panadería"""
#     productos_destacados = Producto.get_all(limit=6)
#     categorias = Categoria.get_all()
#     
#     usuario = get_current_user()
#     carrito_count = get_cart_count()
#     favoritos_ids = get_user_favorites()
#     
#     return render_template('productos/index.html', 
#                          productos=productos_destacados, 
#                          categorias=categorias,
#                          usuario=usuario,
#                          carrito_count=carrito_count,
#                          favoritos_ids=favoritos_ids)

@productos_bp.route('/productos')
def catalogo():
    """Página de catálogo de productos"""
    categoria_id = request.args.get('categoria', type=int)
    busqueda = request.args.get('q', '')
    
    categorias = Categoria.get_all()
    
    if busqueda:
        productos_lista = Producto.search(busqueda)
    else:
        productos_lista = Producto.get_all(categoria_id=categoria_id)
    
    categoria_actual = None
    if categoria_id:
        categoria_actual = Categoria.find_by_id(categoria_id)
    
    usuario = get_current_user()
    carrito_count = get_cart_count()
    favoritos_ids = get_user_favorites()
    
    return render_template('productos/catalogo.html', 
                         productos=productos_lista,
                         categorias=categorias,
                         categoria_actual=categoria_actual,
                         busqueda=busqueda,
                         usuario=usuario,
                         carrito_count=carrito_count,
                         favoritos_ids=favoritos_ids)

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
    favoritos_ids = get_user_favorites()
    
    return render_template('productos/detalle_producto.html',
                         producto=producto,
                         productos_relacionados=productos_relacionados,
                         usuario=usuario,
                         carrito_count=carrito_count,
                         favoritos_ids=favoritos_ids)

@productos_bp.route('/admin/productos')
@admin_or_vendedor_required
def gestionar_productos():
    """Página de gestión de productos para admin y vendedor"""
    productos_lista = Producto.get_all()
    categorias = Categoria.get_all()
    
    return render_template('productos/gestionar.html', 
                         productos=productos_lista,
                         categorias=categorias)

@productos_bp.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@admin_or_vendedor_required
def crear_producto():
    """Crear nuevo producto"""
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.form['nombre'],
                'descripcion': request.form.get('descripcion', ''),
                'precio': float(request.form['precio']),
                'categoria_id': int(request.form['categoria_id']) if request.form.get('categoria_id') else None,
                'stock': int(request.form.get('stock', 0)),
                'imagen': request.form.get('imagen', '')
            }
            
            producto_id = Producto.create(data)
            flash(f'Producto "{data["nombre"]}" creado exitosamente.', 'success')
            return redirect(url_for('productos.gestionar_productos'))
            
        except ValueError as e:
            flash('Error en los datos del producto. Verifica precio y stock.', 'error')
        except Exception as e:
            flash(f'Error al crear el producto: {str(e)}', 'error')
    
    categorias = Categoria.get_all()
    return render_template('productos/crear.html', categorias=categorias)

@productos_bp.route('/admin/productos/<int:producto_id>/editar', methods=['GET', 'POST'])
@admin_or_vendedor_required
def editar_producto(producto_id):
    """Editar producto existente"""
    producto = Producto.find_by_id(producto_id)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos.gestionar_productos'))
    
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.form['nombre'],
                'descripcion': request.form.get('descripcion', ''),
                'precio': float(request.form['precio']),
                'categoria_id': int(request.form['categoria_id']) if request.form.get('categoria_id') else None,
                'stock': int(request.form.get('stock', 0)),
                'imagen': request.form.get('imagen', '')
            }
            
            producto.update(data)
            flash(f'Producto "{data["nombre"]}" actualizado exitosamente.', 'success')
            return redirect(url_for('productos.gestionar_productos'))
            
        except ValueError as e:
            flash('Error en los datos del producto. Verifica precio y stock.', 'error')
        except Exception as e:
            flash(f'Error al actualizar el producto: {str(e)}', 'error')
    
    categorias = Categoria.get_all()
    return render_template('productos/editar.html', producto=producto, categorias=categorias)

@productos_bp.route('/admin/productos/<int:producto_id>/eliminar', methods=['POST'])
@admin_or_vendedor_required
def eliminar_producto(producto_id):
    """Eliminar producto (desactivar)"""
    producto = Producto.find_by_id(producto_id)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos.gestionar_productos'))
    
    try:
        producto.update({'activo': False})
        flash(f'Producto "{producto.nombre}" eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el producto: {str(e)}', 'error')
    
    return redirect(url_for('productos.gestionar_productos'))

# Las rutas de carrito y favoritos ahora están en app/routes/api.py
