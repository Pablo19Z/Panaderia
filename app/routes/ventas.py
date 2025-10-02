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
    cart = session.get('carrito', {})
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
    items_carrito, total = get_cart_from_session()
    
    usuario = get_current_user()
    carrito_count = len(session.get('carrito', {}))
    
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
    items_carrito, total = get_cart_from_session()
    
    if not items_carrito:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('ventas.carrito'))
    
    # Verificar stock disponible
    for item in items_carrito:
        producto = Producto.find_by_id(item[0])  # producto_id está en índice 0
        if item[2] > producto.stock:  # cantidad está en índice 2
            flash(f'Stock insuficiente para {item[3]}', 'error')  # nombre está en índice 3
            return redirect(url_for('ventas.carrito'))
    
    usuario = get_current_user()
    carrito_count = sum(session.get('carrito', {}).values())
    
    cliente = Cliente.find_by_id(session['user_id'])
    
    return render_template('ventas/checkout.html',
                         items=items_carrito,
                         total=total,
                         usuario=usuario,
                         cliente=cliente,
                         carrito_count=carrito_count)

@ventas_bp.route('/procesar_pago', methods=['POST'])
@login_required
def procesar_pago():
    """Procesar el pago y crear el pedido"""
    print("[v0] === INICIO PROCESAR PAGO ===")
    
    direccion_entrega = request.form.get('direccion_entrega')
    telefono_contacto = request.form.get('telefono_contacto')
    fecha_entrega = request.form.get('fecha_entrega')
    hora_entrega = request.form.get('hora_entrega')
    metodo_pago = request.form.get('metodo_pago')
    notas = request.form.get('notas', '')
    
    print(f"[v0] Datos del formulario:")
    print(f"[v0] - Dirección: {direccion_entrega}")
    print(f"[v0] - Teléfono: {telefono_contacto}")
    print(f"[v0] - Fecha: {fecha_entrega}")
    print(f"[v0] - Hora: {hora_entrega}")
    print(f"[v0] - Método de pago: {metodo_pago}")
    print(f"[v0] - Notas: {notas}")
    
    if not direccion_entrega or not telefono_contacto or not fecha_entrega or not hora_entrega or not metodo_pago:
        print("[v0] ERROR: Campos obligatorios faltantes")
        flash('Por favor completa todos los campos obligatorios', 'error')
        return redirect(url_for('ventas.checkout'))
    
    try:
        items_carrito, total = get_cart_from_session()
        print(f"[v0] Items en carrito: {len(items_carrito)}, Total: ${total}")
        
        if not items_carrito:
            print("[v0] ERROR: Carrito vacío")
            flash('Tu carrito está vacío', 'error')
            return redirect(url_for('ventas.carrito'))
        
        print("[v0] Verificando stock de productos...")
        for item in items_carrito:
            producto = Producto.find_by_id(item[0])
            if not producto:
                print(f"[v0] ERROR: Producto {item[0]} no encontrado")
                flash(f'Producto no encontrado', 'error')
                return redirect(url_for('ventas.carrito'))
            
            if item[2] > producto.stock:
                print(f"[v0] ERROR: Stock insuficiente para {producto.nombre}. Solicitado: {item[2]}, Disponible: {producto.stock}")
                flash(f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}', 'error')
                return redirect(url_for('ventas.carrito'))
            
            print(f"[v0] ✓ {producto.nombre}: Stock OK ({item[2]}/{producto.stock})")
        
        print("[v0] Creando pedido en la base de datos...")
        pedido_id = Venta.create({
            'usuario_id': session['user_id'],
            'total': total,
            'direccion_entrega': direccion_entrega,
            'telefono_contacto': telefono_contacto,
            'fecha_entrega': fecha_entrega,
            'hora_entrega': hora_entrega,
            'metodo_pago': metodo_pago,
            'notas': notas
        })
        print(f"[v0] ✓ Pedido creado con ID: {pedido_id}")
        
        # Este precio se guarda en detalle_pedidos.precio_unitario y NUNCA cambia,
        # incluso si el precio del producto se modifica después.
        # Esto garantiza que las ventas históricas mantengan sus precios originales.
        print("[v0] Creando detalles del pedido...")
        detalles = []
        for item in items_carrito:
            producto = Producto.find_by_id(item[0])
            
            detalle = {
                'pedido_id': pedido_id,
                'producto_id': item[0],
                'cantidad': item[2],
                'precio_unitario': producto.precio  # ← Precio capturado al momento de la venta
            }
            detalles.append(detalle)
            print(f"[v0] - {producto.nombre}: {item[2]} x ${producto.precio}")
            
            # Actualizar stock
            print(f"[v0] Actualizando stock de {producto.nombre}: {producto.stock} -> {producto.stock - item[2]}")
            producto.update_stock(-item[2])
        
        # Guardar todos los detalles de la venta
        print("[v0] Guardando detalles en la base de datos...")
        DetalleVenta.create_multiple(detalles)
        print(f"[v0] ✓ {len(detalles)} detalles guardados")
        
        # Vaciar el carrito
        print("[v0] Vaciando carrito...")
        session['carrito'] = {}
        session.permanent = True
        print("[v0] ✓ Carrito vaciado")
        
        numero_pedido = f"ORD-{pedido_id}"
        
        if metodo_pago == 'efectivo':
            flash(f'¡Pedido #{pedido_id} realizado exitosamente! Pago en efectivo al recibir.', 'success')
        elif metodo_pago == 'nequi':
            flash(f'¡Pedido #{pedido_id} realizado exitosamente! Procesando pago por Nequi.', 'success')
        
        print(f"[v0] ✓ Pedido {numero_pedido} completado exitosamente")
        print("[v0] === FIN PROCESAR PAGO (ÉXITO) ===")
        return redirect(url_for('dashboard.cliente'))
        
    except Exception as e:
        print(f"[v0] ❌ ERROR CRÍTICO al procesar pago: {type(e).__name__}")
        print(f"[v0] Mensaje de error: {str(e)}")
        import traceback
        print(f"[v0] Traceback completo:")
        print(traceback.format_exc())
        print("[v0] === FIN PROCESAR PAGO (ERROR) ===")
        
        flash(f'Error al procesar el pedido: {str(e)}. Intenta nuevamente.', 'error')
        return redirect(url_for('ventas.checkout'))
