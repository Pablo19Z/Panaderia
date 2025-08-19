from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.usuario import Usuario
from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.insumo import Insumo
from app.utils.decorators import login_required, role_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    return Usuario.find_by_id(session['user_id'])

def get_cart_count():
    """Obtiene el número de items en el carrito"""
    if 'user_id' not in session:
        return 0
    cliente = Cliente.find_by_id(session['user_id'])
    return cliente.contar_items_carrito() if cliente else 0

@dashboard_bp.route('/cliente')
@role_required('cliente')
def cliente():
    """Dashboard para clientes"""
    usuario = get_current_user()
    cliente_obj = Cliente.find_by_id(session['user_id'])
    
    pedidos_recientes = cliente_obj.get_pedidos()[:5]
    favoritos = cliente_obj.get_favoritos()
    carrito_count = get_cart_count()
    
    return render_template('dashboard/cliente.html', 
                         usuario=usuario, 
                         pedidos=pedidos_recientes,
                         favoritos=favoritos,
                         carrito_count=carrito_count)

@dashboard_bp.route('/admin')
@role_required('admin')
def admin():
    """Dashboard para administradores"""
    usuario = get_current_user()
    estadisticas = Venta.get_estadisticas()
    
    # Estadísticas adicionales
    total_usuarios = Usuario.count()
    from app.models.producto import Producto
    total_productos = len(Producto.get_all())
    
    estadisticas.update({
        'total_usuarios': total_usuarios,
        'total_productos': total_productos
    })
    
    return render_template('dashboard/admin.html', 
                         usuario=usuario, 
                         estadisticas=estadisticas)

@dashboard_bp.route('/vendedor')
@role_required('vendedor')
def vendedor():
    """Dashboard para vendedores"""
    usuario = get_current_user()
    pedidos_pendientes = Venta.get_all(estado='pendiente')
    pedidos_preparando = Venta.get_all(estado='preparando')
    
    return render_template('dashboard/vendedor.html', 
                         usuario=usuario, 
                         pedidos=pedidos_pendientes + pedidos_preparando)

@dashboard_bp.route('/cocinero')
@role_required('cocinero')
def cocinero():
    """Dashboard para cocineros"""
    usuario = get_current_user()
    pedidos_preparacion = Venta.get_all(estado='preparando')
    
    # Obtener detalles de cada pedido
    pedidos_con_detalles = []
    for pedido in pedidos_preparacion:
        detalles = pedido.get_detalles()
        pedidos_con_detalles.append({
            'pedido': pedido,
            'detalles': detalles
        })
    
    return render_template('dashboard/cocinero.html', 
                         usuario=usuario, 
                         pedidos=pedidos_con_detalles)

@dashboard_bp.route('/chef')
@role_required('chef')
def chef():
    """Dashboard para chef/jefe de cocina"""
    usuario = get_current_user()
    insumos_bajo_stock = Insumo.get_low_stock()
    
    # Estadísticas de producción
    estadisticas = Venta.get_estadisticas()
    
    return render_template('dashboard/chef.html', 
                         usuario=usuario, 
                         insumos_bajo_stock=insumos_bajo_stock,
                         estadisticas=estadisticas)
