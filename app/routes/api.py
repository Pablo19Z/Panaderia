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
    
    print(f"[v0] Agregando al carrito - Producto ID: {producto_id}, Cantidad: {cantidad}")
    print(f"[v0] Sesión antes: {session.get('carrito', {})}")
    
    try:
        # Verificar que el producto existe
        producto = Producto.find_by_id(producto_id)
        if not producto:
            return jsonify({'success': False, 'message': 'Producto no encontrado'})
        
        # Verificar stock
        if producto.stock < cantidad:
            return jsonify({'success': False, 'message': 'Stock insuficiente'})
        
        # Inicializar carrito en sesión si no existe
        if 'carrito' not in session:
            session['carrito'] = {}
        
        # Agregar o actualizar cantidad en el carrito
        if producto_id in session['carrito']:
            session['carrito'][producto_id] += cantidad
        else:
            session['carrito'][producto_id] = cantidad
        
        # Verificar que no exceda el stock
        if session['carrito'][producto_id] > producto.stock:
            session['carrito'][producto_id] = producto.stock
        
        session.modified = True
        carrito_count = sum(session['carrito'].values())
        
        print(f"[v0] Sesión después: {session['carrito']}")
        print(f"[v0] Carrito count: {carrito_count}")
        
        return jsonify({
            'success': True, 
            'message': 'Producto agregado al carrito',
            'carrito_count': carrito_count
        })
        
    except Exception as e:
        print(f"[v0] Error agregando al carrito: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al agregar al carrito'})

@api_bp.route('/favoritos/toggle', methods=['POST'])
def toggle_favorito():
    """Toggle favorito (base de datos para usuarios logueados, sesión para no logueados)"""
    data = request.get_json()
    producto_id = str(data.get('producto_id'))
    
    try:
        # Verificar que el producto existe
        producto = Producto.find_by_id(producto_id)
        if not producto:
            return jsonify({'success': False, 'message': 'Producto no encontrado'})
        
        if 'user_id' in session:
            user_id = session['user_id']
            favorito_existente = Favorito.find_by_user_and_product(user_id, producto_id)
            
            if favorito_existente:
                # Eliminar de favoritos
                Favorito.delete(user_id, producto_id)
                es_favorito = False
                mensaje = 'Eliminado de favoritos'
            else:
                # Agregar a favoritos
                Favorito.create(user_id, producto_id)
                es_favorito = True
                mensaje = 'Agregado a favoritos'
        else:
            if 'favoritos' not in session:
                session['favoritos'] = []
            
            if producto_id in session['favoritos']:
                session['favoritos'].remove(producto_id)
                es_favorito = False
                mensaje = 'Eliminado de favoritos'
            else:
                session['favoritos'].append(producto_id)
                es_favorito = True
                mensaje = 'Agregado a favoritos'
            
            session.modified = True
        
        return jsonify({
            'success': True,
            'message': mensaje,
            'es_favorito': es_favorito
        })
        
    except Exception as e:
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
