from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.utils.decorators import login_required, admin_required
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/')
@admin_required
def index():
    """Lista todos los clientes"""
    clientes = Cliente.get_all_clientes()
    return render_template('clientes/index.html', clientes=clientes)

@clientes_bp.route('/crear', methods=['GET', 'POST'])
@admin_required
def crear():
    """Crear un nuevo cliente"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        telefono = request.form.get('telefono', '')
        direccion = request.form.get('direccion', '')
        
        # Validaciones
        if not all([nombre, email, password]):
            flash('Por favor completa todos los campos obligatorios', 'error')
            return render_template('clientes/crear.html')
        
        if Usuario.find_by_email(email):
            flash('Este email ya está registrado', 'error')
            return render_template('clientes/crear.html')
        
        try:
            Usuario.create({
                'nombre': nombre,
                'email': email,
                'password': password,
                'telefono': telefono,
                'direccion': direccion,
                'rol': 'cliente'
            })
            
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('clientes.index'))
            
        except Exception as e:
            flash('Error al crear el cliente', 'error')
    
    return render_template('clientes/crear.html')

@clientes_bp.route('/<int:cliente_id>')
@admin_required
def detalle(cliente_id):
    """Ver detalles de un cliente"""
    cliente = Cliente.find_by_id(cliente_id)
    if not cliente:
        flash('Cliente no encontrado', 'error')
        return redirect(url_for('clientes.index'))
    
    pedidos = cliente.get_pedidos()
    favoritos = cliente.get_favoritos()
    
    return render_template('clientes/detalle.html', 
                         cliente=cliente, 
                         pedidos=pedidos,
                         favoritos=favoritos)

@clientes_bp.route('/<int:cliente_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar(cliente_id):
    """Editar un cliente"""
    cliente = Cliente.find_by_id(cliente_id)
    if not cliente:
        flash('Cliente no encontrado', 'error')
        return redirect(url_for('clientes.index'))
    
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'telefono': request.form.get('telefono', ''),
            'direccion': request.form.get('direccion', '')
        }
        
        # Verificar email único (excepto el actual)
        existing_user = Usuario.find_by_email(data['email'])
        if existing_user and existing_user.id != cliente_id:
            flash('Este email ya está en uso por otro usuario', 'error')
            return render_template('clientes/editar.html', cliente=cliente)
        
        try:
            cliente.update(data)
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('clientes.detalle', cliente_id=cliente_id))
            
        except Exception as e:
            flash('Error al actualizar el cliente', 'error')
    
    return render_template('clientes/editar.html', cliente=cliente)

@clientes_bp.route('/api/chatbot/mensaje', methods=['POST'])
@login_required
def chatbot_mensaje():
    """API para el chatbot - respuestas automáticas"""
    data = request.get_json()
    mensaje_usuario = data.get('mensaje', '').lower().strip()
    
    if not mensaje_usuario:
        return jsonify({'success': False, 'message': 'Mensaje vacío'})
    
    from instance.config import InstanceConfig
    respuestas_bot = InstanceConfig.CHATBOT_RESPONSES
    
    # Buscar respuesta basada en palabras clave
    respuesta_bot = "Lo siento, no entiendo tu consulta. ¿Podrías ser más específico? Puedo ayudarte con información sobre horarios, ubicación, delivery, especialidades, pedidos o contacto."
    
    for palabra_clave, respuesta in respuestas_bot.items():
        if palabra_clave in mensaje_usuario:
            respuesta_bot = respuesta
            break
    
    # Guardar conversación en la base de datos (implementar si es necesario)
    
    return jsonify({
        'success': True,
        'respuesta': respuesta_bot,
        'timestamp': datetime.now().strftime('%H:%M')
    })

@clientes_bp.route('/chatbot')
@login_required
def chatbot():
    """Página del chatbot"""
    from app.models.usuario import Usuario
    usuario = Usuario.find_by_id(session['user_id'])
    cliente = Cliente.find_by_id(session['user_id'])
    carrito_count = cliente.contar_items_carrito() if cliente else 0
    
    return render_template('chatbot.html',
                         usuario=usuario,
                         carrito_count=carrito_count)
