from flask import Blueprint, request, jsonify, session, make_response
from app.models.producto import Producto
from app.models.carrito import Carrito
from app.models.favorito import Favorito
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    """Agregar producto al carrito (funciona sin login usando sesiones)"""
    data = request.get_json()
    producto_id = str(data.get('producto_id'))
    cantidad = int(data.get('cantidad', 1))
    
    print(f"[v0] === INICIO AGREGAR AL CARRITO ===")
    print(f"[v0] Producto ID: {producto_id}, Cantidad: {cantidad}")
    print(f"[v0] Sesión completa antes: {dict(session)}")
    print(f"[v0] Carrito antes: {session.get('carrito', {})}")
    
    try:
        # Verificar que el producto existe
        producto = Producto.find_by_id(producto_id)
        if not producto:
            print(f"[v0] ERROR: Producto {producto_id} no encontrado")
            return jsonify({'success': False, 'message': 'Producto no encontrado'})
        
        print(f"[v0] Producto encontrado: {producto.nombre}, Stock: {producto.stock}")
        
        # Verificar stock
        if producto.stock < cantidad:
            print(f"[v0] ERROR: Stock insuficiente. Solicitado: {cantidad}, Disponible: {producto.stock}")
            return jsonify({'success': False, 'message': 'Stock insuficiente'})
        
        # Inicializar carrito en sesión si no existe
        if 'carrito' not in session:
            session['carrito'] = {}
            print(f"[v0] Carrito inicializado vacío")
        
        # Agregar o actualizar cantidad en el carrito
        if producto_id in session['carrito']:
            cantidad_anterior = session['carrito'][producto_id]
            session['carrito'][producto_id] += cantidad
            print(f"[v0] Cantidad actualizada: {cantidad_anterior} -> {session['carrito'][producto_id]}")
        else:
            session['carrito'][producto_id] = cantidad
            print(f"[v0] Producto agregado por primera vez con cantidad: {cantidad}")
        
        # Verificar que no exceda el stock
        if session['carrito'][producto_id] > producto.stock:
            session['carrito'][producto_id] = producto.stock
            print(f"[v0] Cantidad ajustada al stock máximo: {producto.stock}")
        
        session.modified = True
        session.permanent = True
        
        carrito_count = sum(session['carrito'].values())
        
        print(f"[v0] Carrito después: {session['carrito']}")
        print(f"[v0] Sesión completa después: {dict(session)}")
        print(f"[v0] Total items en carrito: {carrito_count}")
        print(f"[v0] === FIN AGREGAR AL CARRITO ===")
        
        return jsonify({
            'success': True, 
            'message': 'Producto agregado al carrito exitosamente',
            'carrito_count': carrito_count
        })
        
    except Exception as e:
        print(f"[v0] ERROR CRÍTICO: {str(e)}")
        import traceback
        print(f"[v0] Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': 'Error al agregar al carrito'})

@api_bp.route('/carrito/actualizar', methods=['POST'])
def actualizar_carrito():
    """Actualizar cantidad de un producto en el carrito"""
    data = request.get_json()
    producto_id = str(data.get('producto_id'))
    cantidad = int(data.get('cantidad', 1))
    
    try:
        # Verificar que el producto existe
        producto = Producto.find_by_id(producto_id)
        if not producto:
            return jsonify({'success': False, 'message': 'Producto no encontrado'})
        
        # Verificar stock
        if cantidad > producto.stock:
            return jsonify({'success': False, 'message': f'Solo hay {producto.stock} unidades disponibles'})
        
        if cantidad <= 0:
            return jsonify({'success': False, 'message': 'La cantidad debe ser mayor a 0'})
        
        # Inicializar carrito si no existe
        if 'carrito' not in session:
            session['carrito'] = {}
        
        # Actualizar cantidad
        session['carrito'][producto_id] = cantidad
        session.modified = True
        
        carrito_count = sum(session['carrito'].values())
        
        return jsonify({
            'success': True,
            'message': 'Cantidad actualizada',
            'carrito_count': carrito_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al actualizar carrito'})

@api_bp.route('/carrito/eliminar', methods=['POST'])
def eliminar_del_carrito():
    """Eliminar un producto del carrito"""
    data = request.get_json()
    producto_id = str(data.get('producto_id'))
    
    try:
        if 'carrito' not in session:
            session['carrito'] = {}
        
        if producto_id in session['carrito']:
            del session['carrito'][producto_id]
            session.modified = True
        
        carrito_count = sum(session['carrito'].values())
        
        return jsonify({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'carrito_count': carrito_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al eliminar producto'})

@api_bp.route('/carrito/vaciar', methods=['POST'])
def vaciar_carrito():
    """Vaciar todo el carrito"""
    try:
        session['carrito'] = {}
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Carrito vaciado exitosamente',
            'carrito_count': 0
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al vaciar carrito'})

@api_bp.route('/favoritos/toggle', methods=['POST'])
def toggle_favorito():
    """Toggle favorito (base de datos para usuarios logueados, sesión para no logueados)"""
    data = request.get_json()
    producto_id = str(data.get('producto_id'))
    
    print(f"[v0] === TOGGLE FAVORITO ===")
    print(f"[v0] Producto ID: {producto_id}")
    print(f"[v0] Usuario logueado: {'user_id' in session}")
    print(f"[v0] Sesión: {dict(session)}")
    
    try:
        # Verificar que el producto existe
        producto = Producto.find_by_id(producto_id)
        if not producto:
            print(f"[v0] ERROR: Producto {producto_id} no encontrado")
            return jsonify({'success': False, 'message': 'Producto no encontrado'})
        
        if 'user_id' in session:
            user_id = session['user_id']
            print(f"[v0] Usuario logueado ID: {user_id}")
            
            favorito_existente = Favorito.find_by_user_and_product(user_id, producto_id)
            print(f"[v0] Favorito existente: {favorito_existente}")
            
            if favorito_existente:
                # Eliminar de favoritos
                Favorito.delete(user_id, producto_id)
                es_favorito = False
                mensaje = 'Eliminado de favoritos'
                print(f"[v0] Favorito eliminado")
            else:
                # Agregar a favoritos
                Favorito.create(user_id, producto_id)
                es_favorito = True
                mensaje = 'Agregado a favoritos'
                print(f"[v0] Favorito agregado")
        else:
            print(f"[v0] Usuario no logueado, usando sesión")
            if 'favoritos' not in session:
                session['favoritos'] = []
            
            print(f"[v0] Favoritos en sesión antes: {session['favoritos']}")
            
            if producto_id in session['favoritos']:
                session['favoritos'].remove(producto_id)
                es_favorito = False
                mensaje = 'Eliminado de favoritos'
                print(f"[v0] Favorito eliminado de sesión")
            else:
                session['favoritos'].append(producto_id)
                es_favorito = True
                mensaje = 'Agregado a favoritos'
                print(f"[v0] Favorito agregado a sesión")
            
            session.modified = True
            print(f"[v0] Favoritos en sesión después: {session['favoritos']}")
        
        print(f"[v0] Resultado: {mensaje}, es_favorito: {es_favorito}")
        print(f"[v0] === FIN TOGGLE FAVORITO ===")
        
        return jsonify({
            'success': True,
            'message': mensaje,
            'es_favorito': es_favorito
        })
        
    except Exception as e:
        print(f"[v0] ERROR CRÍTICO en favoritos: {str(e)}")
        import traceback
        print(f"[v0] Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': 'Error al gestionar favoritos'})

@api_bp.route('/carrito/count', methods=['GET'])
def get_carrito_count():
    """Obtener cantidad de items en el carrito"""
    carrito = session.get('carrito', {})
    count = sum(carrito.values())
    return jsonify({'carrito_count': count})

@api_bp.route('/favoritos/check/<producto_id>', methods=['GET'])
def check_favorito(producto_id):
    """Verificar si un producto está en favoritos"""
    if 'user_id' in session:
        user_id = session['user_id']
        favorito_existente = Favorito.find_by_user_and_product(user_id, producto_id)
        es_favorito = favorito_existente is not None
    else:
        # Para usuarios no logueados, verificar en sesión
        favoritos = session.get('favoritos', [])
        es_favorito = str(producto_id) in favoritos
    
    return jsonify({'es_favorito': es_favorito})

@api_bp.route('/pedido/<int:pedido_id>/recibo-pdf', methods=['GET'])
def generar_recibo_pdf(pedido_id):
    """Generar PDF del recibo de un pedido"""
    try:
        # Verificar que el usuario esté logueado
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Usuario no autenticado'}), 401
        
        # Obtener el pedido
        venta = Venta.find_by_id(pedido_id)
        if not venta:
            return jsonify({'success': False, 'message': 'Pedido no encontrado'}), 404
        
        # Verificar que el pedido pertenece al usuario actual
        if venta.usuario_id != session['user_id']:
            return jsonify({'success': False, 'message': 'No autorizado'}), 403
        
        detalles = DetalleVenta.get_by_pedido(pedido_id)
        
        # Crear PDF en memoria
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Colores
        gold_color = HexColor('#d4af37')
        dark_color = HexColor('#1a1a1a')
        
        # Header con logo igual al de la página principal
        p.setFillColor(gold_color)
        p.setFont("Helvetica-Bold", 28)
        p.drawCentredString(width/2, height-40, "🍞 Migas de oro Dorè")
        
        p.setFillColor(dark_color)
        p.setFont("Helvetica-Oblique", 14)
        p.drawCentredString(width/2, height-65, "Panadería Artesanal")
        p.setFont("Helvetica", 10)
        p.drawCentredString(width/2, height-80, "NIT: 123.456.789-0 | Reg. Sanitario: RS-2024-001")
        
        # Línea separadora
        p.setStrokeColor(gold_color)
        p.setLineWidth(2)
        p.line(50, height-95, width-50, height-95)
        
        # Información del pedido
        y_pos = height - 125
        p.setFillColor(dark_color)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_pos, f"RECIBO - Pedido #{pedido_id}")
        
        y_pos -= 30
        p.setFont("Helvetica", 11)
        p.drawString(50, y_pos, f"Fecha: {venta.fecha_pedido.strftime('%d/%m/%Y %H:%M') if venta.fecha_pedido else 'N/A'}")
        p.drawString(300, y_pos, f"Estado: {venta.estado.upper()}")
        
        y_pos -= 20
        p.drawString(50, y_pos, f"Cliente: {session.get('user_name', 'N/A')}")
        p.drawString(300, y_pos, f"Teléfono: {venta.telefono_contacto or 'N/A'}")
        
        y_pos -= 20
        p.drawString(50, y_pos, f"Dirección: {venta.direccion_entrega or 'N/A'}")
        
        # Línea separadora
        y_pos -= 30
        p.setStrokeColor(gold_color)
        p.line(50, y_pos, width-50, y_pos)
        
        # Detalles de productos
        y_pos -= 30
        p.setFillColor(gold_color)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_pos, "DETALLE DE PRODUCTOS")
        
        y_pos -= 25
        p.setFillColor(dark_color)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y_pos, "Producto")
        p.drawString(250, y_pos, "Cantidad")
        p.drawString(320, y_pos, "Precio Unit.")
        p.drawString(420, y_pos, "Subtotal")
        
        y_pos -= 5
        p.setStrokeColor(dark_color)
        p.line(50, y_pos, width-50, y_pos)
        
        def format_cop(amount):
            """Formatear cantidad en pesos colombianos"""
            return f"${amount:,.0f}".replace(",", ".")
        
        # Productos
        y_pos -= 20
        p.setFont("Helvetica", 10)
        total_productos = 0
        
        for detalle in detalles:
            if y_pos < 100:  # Nueva página si es necesario
                p.showPage()
                y_pos = height - 50
            
            producto = Producto.find_by_id(detalle.producto_id)
            if producto:
                subtotal = detalle.cantidad * detalle.precio_unitario
                total_productos += subtotal
                
                p.drawString(50, y_pos, producto.nombre[:30])
                p.drawString(250, y_pos, str(detalle.cantidad))
                p.drawString(320, y_pos, format_cop(detalle.precio_unitario))
                p.drawString(420, y_pos, format_cop(subtotal))
                y_pos -= 15
        
        # Total
        y_pos -= 20
        p.setStrokeColor(gold_color)
        p.setLineWidth(2)
        p.line(300, y_pos, width-50, y_pos)
        
        y_pos -= 25
        p.setFillColor(gold_color)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(320, y_pos, f"TOTAL: {format_cop(venta.total)}")
        
        # Método de pago
        y_pos -= 30
        p.setFillColor(dark_color)
        p.setFont("Helvetica", 11)
        metodo_pago_display = "Nequi" if venta.metodo_pago == "nequi" else "Efectivo" if venta.metodo_pago == "efectivo" else venta.metodo_pago.title()
        p.drawString(50, y_pos, f"Método de pago: {metodo_pago_display}")
        
        if venta.notas:
            y_pos -= 20
            p.drawString(50, y_pos, f"Notas: {venta.notas}")
        
        # Footer
        y_pos = 80
        p.setFillColor(gold_color)
        p.setFont("Helvetica-Bold", 12)
        p.drawCentredString(width/2, y_pos, "¡Gracias por tu pedido!")
        
        y_pos -= 20
        p.setFillColor(dark_color)
        p.setFont("Helvetica", 9)
        p.drawCentredString(width/2, y_pos, "Contacto: +57 300 123 4567 | info@migasdeorodoré.com")
        
        # Finalizar PDF
        p.save()
        buffer.seek(0)
        
        # Crear respuesta
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=recibo-pedido-{pedido_id}.pdf'
        
        return response
        
    except Exception as e:
        print(f"[v0] ERROR al generar PDF: {str(e)}")
        import traceback
        print(f"[v0] Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': 'Error al generar PDF'}), 500
