from flask import Blueprint, request, jsonify, session
from app.models.producto import Producto
from app.models.carrito import Carrito
from app.models.favorito import Favorito
import sqlite3

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
