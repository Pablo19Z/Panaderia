from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.utils.decorators import login_required

ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    from app.models.usuario import Usuario
    return Usuario.find_by_id(session['user_id'])

def get_cart_from_session():
    """Obtiene items del carrito desde la sesión"""
    cart = session.get('cart', {})
    items = []
    total = 0
    
    for producto_id, cantidad in cart.items():
        producto = Producto.find_by_id(producto_id)
        if producto:
            item = (
                int(producto_id),  # 0: id
                session.get('user_id', 0),  # 1: usuario_id
                cantidad,  # 2: cantidad
                producto.nombre,  # 3: nombre
                producto.precio,  # 4: precio
                producto.stock,  # 5: stock
                producto.imagen_url  # 6: imagen
            )
            items.append(item)
            total += producto.precio * cantidad
    
    return items, total

@ventas_bp.route('/carrito')
def carrito():
    """Página del carrito de compras (funciona sin login)"""
    print(f"[v0] Sesión completa: {dict(session)}")
    print(f"[v0] Carrito en sesión: {session.get('cart', {})}")
    
    items_carrito, total = get_cart_from_session()
    print(f"[v0] Items del carrito obtenidos: {items_carrito}")
    print(f"[v0] Total calculado: {total}")
    
    usuario = get_current_user()
    carrito_count = len(session.get('cart', {}))
    
    return render_template('carrito.html',
                         items=items_carrito,
                         total=total,
                         usuario=usuario,
                         carrito_count=carrito_count)

@ventas_bp.route('/api/carrito/actualizar', methods=['POST'])
@login_required
def actualizar_carrito():
    """API para actualizar cantidad de items en el carrito"""
    data = request.get_json()
    item_id = data.get('item_id')
    nueva_cantidad = data.get('cantidad')
    
    if not item_id or nueva_cantidad < 1:
        return jsonify({'success': False, 'message': 'Datos inválidos'})
    
    try:
        # Lógica para actualizar carrito (implementar en modelo Cliente)
        cliente = Cliente.find_by_id(session['user_id'])
        # Aquí iría la lógica de actualización
        carrito_count = cliente.contar_items_carrito()
        
        return jsonify({
            'success': True,
            'message': 'Carrito actualizado',
            'carrito_count': carrito_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al actualizar carrito'})

@ventas_bp.route('/api/carrito/eliminar', methods=['POST'])
@login_required
def eliminar_del_carrito():
    """API para eliminar items del carrito"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({'success': False, 'message': 'Item no especificado'})
    
    try:
        # Lógica para eliminar del carrito
        cliente = Cliente.find_by_id(session['user_id'])
        carrito_count = cliente.contar_items_carrito()
        
        return jsonify({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'carrito_count': carrito_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al eliminar del carrito'})

@ventas_bp.route('/api/carrito/vaciar', methods=['POST'])
@login_required
def vaciar_carrito():
    """API para vaciar completamente el carrito"""
    try:
        cliente = Cliente.find_by_id(session['user_id'])
        cliente.vaciar_carrito()
        
        return jsonify({
            'success': True,
            'message': 'Carrito vaciado',
            'carrito_count': 0
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al vaciar carrito'})

@ventas_bp.route('/checkout')
@login_required
def checkout():
    """Página de checkout/pago"""
    cliente = Cliente.find_by_id(session['user_id'])
    items_carrito = cliente.get_carrito()
    
    if not items_carrito:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('ventas.carrito'))
    
    # Verificar stock disponible
    for item in items_carrito:
        producto = Producto.find_by_id(item[2])  # producto_id
        if item[3] > producto.stock:  # cantidad > stock
            flash(f'Stock insuficiente para {item[4]}', 'error')  # nombre
            return redirect(url_for('ventas.carrito'))
    
    total = cliente.get_total_carrito()
    usuario = get_current_user()
    carrito_count = len(session.get('cart', {}))
    
    return render_template('checkout.html',
                         items=items_carrito,
                         total=total,
                         usuario=usuario,
                         carrito_count=carrito_count)

@ventas_bp.route('/procesar_pago', methods=['POST'])
@login_required
def procesar_pago():
    """Procesar el pago y crear el pedido"""
    direccion_entrega = request.form.get('direccion_entrega')
    telefono_contacto = request.form.get('telefono_contacto')
    notas = request.form.get('notas', '')
    
    if not direccion_entrega or not telefono_contacto:
        flash('Por favor completa todos los campos obligatorios', 'error')
        return redirect(url_for('ventas.checkout'))
    
    try:
        cliente = Cliente.find_by_id(session['user_id'])
        items_carrito = cliente.get_carrito()
        
        if not items_carrito:
            flash('Tu carrito está vacío', 'error')
            return redirect(url_for('ventas.carrito'))
        
        total = cliente.get_total_carrito()
        
        # Crear pedido
        pedido_id = Venta.create({
            'usuario_id': session['user_id'],
            'total': total,
            'direccion_entrega': direccion_entrega,
            'telefono_contacto': telefono_contacto,
            'notas': notas
        })
        
        # Crear detalles del pedido y actualizar stock
        detalles = []
        for item in items_carrito:
            producto = Producto.find_by_id(item[2])
            detalles.append({
                'pedido_id': pedido_id,
                'producto_id': item[2],
                'cantidad': item[3],
                'precio_unitario': producto.precio
            })
            
            # Actualizar stock del producto
            producto.update_stock(-item[3])
        
        DetalleVenta.create_multiple(detalles)
        
        # Vaciar carrito
        cliente.vaciar_carrito()
        
        flash('¡Pedido realizado exitosamente! Te contactaremos pronto.', 'success')
        return redirect(url_for('dashboard.cliente'))
        
    except Exception as e:
        flash('Error al procesar el pedido. Intenta nuevamente.', 'error')
        return redirect(url_for('ventas.checkout'))
