from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models.usuario import Usuario
from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.insumo import Insumo
from app.models.producto import Producto
from app.models.movimientos_inventario import MovimientoInventario
from app.utils.decorators import login_required, role_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    return Usuario.find_by_id(session['user_id'])

def get_cart_count():
    """Obtiene el número de items en el carrito"""
    carrito = session.get('carrito', {})
    return sum(carrito.values())

@dashboard_bp.route('/cliente')
@role_required('cliente')
def cliente():
    """Dashboard para clientes"""
    usuario = get_current_user()
    cliente_obj = Cliente.find_by_id(session['user_id'])
    
    if not cliente_obj:
        flash('Error: No se pudo cargar la información del cliente. Por favor, inicia sesión nuevamente.', 'error')
        return redirect(url_for('auth.logout'))
    
    try:
        pedidos_recientes = cliente_obj.get_pedidos()[:5]
        favoritos = cliente_obj.get_favoritos()
    except Exception as e:
        print(f"[v0] Error obteniendo datos del cliente: {e}")
        pedidos_recientes = []
        favoritos = []
        flash('Error al cargar algunos datos del perfil.', 'warning')
    
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
    total_productos = len(Producto.get_all())
    
    estadisticas.update({
        'total_usuarios': total_usuarios,
        'total_productos': total_productos
    })
    
    return render_template('dashboard/admin.html', 
                         usuario=usuario, 
                         estadisticas=estadisticas)

@dashboard_bp.route('/admin/usuarios')
@role_required('admin')
def admin_usuarios():
    """Gestión de usuarios para administradores"""
    usuarios = Usuario.get_all()
    return render_template('dashboard/admin_usuarios.html', usuarios=usuarios)

@dashboard_bp.route('/admin/crear_usuario', methods=['GET', 'POST'])
@role_required('admin')
def admin_crear_usuario():
    """Crear nuevo usuario (vendedor, chef, cocinero)"""
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.form['nombre'],
                'email': request.form['email'],
                'password': request.form['password'],
                'telefono': request.form.get('telefono', ''),
                'direccion': request.form.get('direccion', ''),
                'rol': request.form['rol']
            }
            
            # Validar que el email no exista
            if Usuario.find_by_email(data['email']):
                flash('Este email ya está registrado', 'error')
                return render_template('dashboard/admin_crear_usuario.html')
            
            # Validar rol
            if data['rol'] not in ['vendedor', 'chef', 'cocinero']:
                flash('Rol no válido', 'error')
                return render_template('dashboard/admin_crear_usuario.html')
            
            user_id = Usuario.create(data)
            flash(f'Usuario {data["nombre"]} creado exitosamente como {data["rol"]}', 'success')
            return redirect(url_for('dashboard.admin_usuarios'))
            
        except Exception as e:
            flash('Error al crear usuario', 'error')
            print(f"Error creando usuario: {e}")
    
    return render_template('dashboard/admin_crear_usuario.html')

@dashboard_bp.route('/admin/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def admin_editar_usuario(user_id):
    """Editar usuario existente"""
    usuario_edit = Usuario.find_by_id(user_id)
    if not usuario_edit:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('dashboard.admin_usuarios'))
    
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.form['nombre'],
                'email': request.form['email'],
                'telefono': request.form.get('telefono', ''),
                'direccion': request.form.get('direccion', ''),
                'rol': request.form['rol'],
                'activo': 1 if request.form.get('activo') else 0
            }
            
            # Solo actualizar contraseña si se proporciona
            if request.form.get('password'):
                data['password'] = request.form['password']
            
            Usuario.update(user_id, data)
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('dashboard.admin_usuarios'))
            
        except Exception as e:
            flash('Error al actualizar usuario', 'error')
            print(f"Error actualizando usuario: {e}")
    
    return render_template('dashboard/admin_editar_usuario.html', usuario_edit=usuario_edit)

@dashboard_bp.route('/admin/toggle_usuario/<int:user_id>')
@role_required('admin')
def admin_toggle_usuario(user_id):
    """Activar/desactivar usuario"""
    try:
        usuario_edit = Usuario.find_by_id(user_id)
        if usuario_edit:
            nuevo_estado = 0 if usuario_edit.activo else 1
            Usuario.update(user_id, {'activo': nuevo_estado})
            estado_texto = 'activado' if nuevo_estado else 'desactivado'
            flash(f'Usuario {estado_texto} exitosamente', 'success')
        else:
            flash('Usuario no encontrado', 'error')
    except Exception as e:
        flash('Error al cambiar estado del usuario', 'error')
        print(f"Error toggle usuario: {e}")
    
    return redirect(url_for('dashboard.admin_usuarios'))

@dashboard_bp.route('/admin/productos')
@role_required('admin')
def admin_productos():
    """Gestión de productos para administradores"""
    productos = Producto.get_all()
    return render_template('dashboard/admin_productos.html', productos=productos)

@dashboard_bp.route('/admin/ventas')
@role_required('admin')
def admin_ventas():
    """Gestión de ventas para administradores"""
    ventas = Venta.get_all()
    return render_template('dashboard/admin_ventas.html', ventas=ventas)

@dashboard_bp.route('/vendedor')
@role_required('vendedor')
def vendedor():
    """Dashboard para vendedores"""
    usuario = get_current_user()
    
    # Pedidos por estado
    pedidos_pendientes = Venta.get_all(estado='pendiente')
    pedidos_preparando = Venta.get_all(estado='preparando')
    pedidos_listos = Venta.get_all(estado='listo')
    
    # Productos más vendidos
    productos_populares = Producto.get_mas_vendidos(5)
    
    # Estadísticas del día
    estadisticas = Venta.get_estadisticas()
    
    return render_template('dashboard/vendedor.html', 
                         usuario=usuario, 
                         pedidos_pendientes=pedidos_pendientes,
                         pedidos_preparando=pedidos_preparando,
                         pedidos_listos=pedidos_listos,
                         productos_populares=productos_populares,
                         estadisticas=estadisticas)

@dashboard_bp.route('/vendedor/actualizar_pedido/<int:pedido_id>/<estado>')
@role_required('vendedor')
def vendedor_actualizar_pedido(pedido_id, estado):
    """Actualizar estado de pedido"""
    try:
        pedido = Venta.find_by_id(pedido_id)
        if pedido:
            pedido.update_estado(estado)
            flash(f'Pedido #{pedido_id} actualizado a {estado}', 'success')
        else:
            flash('Pedido no encontrado', 'error')
    except Exception as e:
        flash('Error al actualizar pedido', 'error')
        print(f"Error actualizando pedido: {e}")
    
    return redirect(url_for('dashboard.vendedor'))

@dashboard_bp.route('/chef')
@role_required('chef')
def chef():
    """Dashboard para chef/jefe de cocina con funcionalidades de producción"""
    usuario = get_current_user()
    
    # Pedidos en preparación (funcionalidad transferida de cocinero)
    pedidos_preparacion = Venta.get_all(estado='preparando')
    
    # Obtener detalles de cada pedido
    pedidos_con_detalles = []
    for pedido in pedidos_preparacion:
        detalles = pedido.get_detalles()
        pedidos_con_detalles.append({
            'pedido': pedido,
            'detalles': detalles
        })
    
    # Insumos con stock bajo
    insumos_bajo_stock = Insumo.get_low_stock()
    
    # Estadísticas completas
    estadisticas = Venta.get_estadisticas()
    
    # Todos los insumos para gestión
    todos_insumos = Insumo.get_all()
    
    # Movimientos recientes
    movimientos_recientes = MovimientoInventario.get_movimientos_recientes(15)
    
    # Productos más vendidos para planificación
    productos_populares = Producto.get_mas_vendidos(10)
    
    return render_template('dashboard/chef.html', 
                         usuario=usuario, 
                         pedidos=pedidos_con_detalles,
                         insumos_bajo_stock=insumos_bajo_stock,
                         estadisticas=estadisticas,
                         todos_insumos=todos_insumos,
                         movimientos_recientes=movimientos_recientes,
                         productos_populares=productos_populares)

@dashboard_bp.route('/chef/usar_insumo', methods=['POST'])
@role_required('chef')
def chef_usar_insumo():
    """Registrar uso de insumo en producción (funcionalidad transferida de cocinero)"""
    try:
        insumo_id = request.form['insumo_id']
        cantidad = float(request.form['cantidad'])
        motivo = request.form.get('motivo', 'Uso en producción')
        
        MovimientoInventario.registrar_salida(
            insumo_id=insumo_id,
            cantidad=cantidad,
            motivo=motivo,
            usuario_id=session['user_id']
        )
        
        flash('Uso de insumo registrado correctamente', 'success')
    except Exception as e:
        flash('Error al registrar uso de insumo', 'error')
        print(f"Error registrando uso de insumo: {e}")
    
    return redirect(url_for('dashboard.chef'))

@dashboard_bp.route('/chef/marcar_listo/<int:pedido_id>')
@role_required('chef')
def chef_marcar_listo(pedido_id):
    """Marcar pedido como listo (funcionalidad transferida de cocinero)"""
    try:
        pedido = Venta.find_by_id(pedido_id)
        if pedido:
            pedido.update_estado('listo')
            flash(f'Pedido #{pedido_id} marcado como listo', 'success')
        else:
            flash('Pedido no encontrado', 'error')
    except Exception as e:
        flash('Error al actualizar pedido', 'error')
        print(f"Error actualizando pedido: {e}")
    
    return redirect(url_for('dashboard.chef'))

@dashboard_bp.route('/chef/agregar_insumo', methods=['POST'])
@role_required('chef')
def chef_agregar_insumo():
    """Agregar entrada de insumo"""
    try:
        insumo_id = request.form['insumo_id']
        cantidad = float(request.form['cantidad'])
        motivo = request.form.get('motivo', 'Compra de insumos')
        
        MovimientoInventario.registrar_entrada(
            insumo_id=insumo_id,
            cantidad=cantidad,
            motivo=motivo,
            usuario_id=session['user_id']
        )
        
        flash('Entrada de insumo registrada correctamente', 'success')
    except Exception as e:
        flash('Error al registrar entrada de insumo', 'error')
        print(f"Error registrando entrada de insumo: {e}")
    
    return redirect(url_for('dashboard.chef'))

@dashboard_bp.route('/chef/crear_insumo', methods=['POST'])
@role_required('chef')
def chef_crear_insumo():
    """Crear nuevo insumo"""
    try:
        data = {
            'nombre': request.form['nombre'],
            'descripcion': request.form.get('descripcion', ''),
            'cantidad_actual': float(request.form.get('cantidad_inicial', 0)),
            'cantidad_minima': float(request.form.get('cantidad_minima', 0)),
            'unidad_medida': request.form.get('unidad_medida', 'kg'),
            'precio_compra': float(request.form.get('precio_compra', 0)),
            'proveedor': request.form.get('proveedor', '')
        }
        
        insumo_id = Insumo.create(data)
        flash(f'Insumo "{data["nombre"]}" creado correctamente', 'success')
        
        # Registrar movimiento inicial si hay cantidad
        if data['cantidad_actual'] > 0:
            MovimientoInventario.registrar_entrada(
                insumo_id=insumo_id,
                cantidad=data['cantidad_actual'],
                motivo='Stock inicial',
                usuario_id=session['user_id']
            )
        
    except Exception as e:
        flash('Error al crear insumo', 'error')
        print(f"Error creando insumo: {e}")
    
    return redirect(url_for('dashboard.chef'))

@dashboard_bp.route('/chef/calcular_costos')
@role_required('chef')
def chef_calcular_costos():
    """Calcular costos de producción"""
    try:
        # Obtener estadísticas de ventas
        estadisticas = Venta.get_estadisticas()
        
        # Calcular costos de insumos del mes
        insumos = Insumo.get_all()
        costo_total_insumos = sum(
            (insumo.precio_compra or 0) * (insumo.cantidad_actual or 0) 
            for insumo in insumos
        )
        
        # Calcular margen de ganancia
        ventas_mes = estadisticas.get('ventas_mes', {}).get('total', 0)
        margen_ganancia = ventas_mes - costo_total_insumos if ventas_mes > 0 else 0
        porcentaje_margen = (margen_ganancia / ventas_mes * 100) if ventas_mes > 0 else 0
        
        costos = {
            'costo_insumos': costo_total_insumos,
            'ventas_mes': ventas_mes,
            'margen_ganancia': margen_ganancia,
            'porcentaje_margen': porcentaje_margen
        }
        
        return jsonify(costos)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
