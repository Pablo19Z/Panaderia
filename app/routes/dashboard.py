from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models.usuario import Usuario
from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.insumo import Insumo
from app.models.system_settings import SystemSettings
from app.models.historia_images import HistoriaImages
from app.utils.decorators import login_required, role_required, admin_required
from datetime import datetime
import secrets
import string
import os
from werkzeug.utils import secure_filename

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

UPLOAD_FOLDER = 'static/comprobantes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    
    usuario = Usuario.find_by_id(session['user_id'])
    
    # Si el usuario no existe (base de datos reiniciada), limpiar sesión
    if not usuario:
        session.clear()
        return None
    
    return usuario

def get_cart_count():
    """Obtiene el número de items en el carrito"""
    carrito = session.get('carrito', {})
    return sum(carrito.values())

def generar_password_temporal():
    """Genera una contraseña temporal de 8 caracteres"""
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(8))

@dashboard_bp.route('/cliente')
@role_required('cliente')
def cliente():
    """Dashboard para clientes"""
    usuario = get_current_user()
    
    if not usuario:
        flash('Error: No se pudo cargar el perfil del usuario', 'error')
        return redirect(url_for('index'))
    
    # Obtener pedidos recientes del usuario usando get_all con filtro usuario_id
    try:
        pedidos_recientes = Venta.get_all(usuario_id=session['user_id'])[:5]
    except Exception as e:
        pedidos_recientes = []
    
    carrito_count = get_cart_count()
    
    return render_template('dashboard/cliente.html', 
                         usuario=usuario, 
                         pedidos=pedidos_recientes,
                         carrito_count=carrito_count)

@dashboard_bp.route('/admin')
@admin_required
def admin():
    """Dashboard para administradores"""
    usuario = get_current_user()
    estadisticas = Venta.get_estadisticas()
    
    total_chefs = Usuario.count_by_role('chef')
    total_vendedores = Usuario.count_by_role('vendedor')
    total_usuarios = Usuario.count()
    
    from app.models.producto import Producto
    total_productos = len(Producto.get_all())
    
    estadisticas.update({
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_chefs': total_chefs,
        'total_vendedores': total_vendedores
    })
    
    fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    try:
        SystemSettings.create_table()  # Asegurar que la tabla existe
        hero_background_url = SystemSettings.get_setting('hero_background_url') or '/placeholder.svg?height=600&width=1200'
        
        HistoriaImages.create_table()
        historia_images_data = HistoriaImages.get_all_images()
        
        # Convert to simple dict with just URLs
        historia_images = {
            'inicios_image': historia_images_data.get('inicios_image', {}).get('url', '/placeholder.svg?height=400&width=600'),
            'timeline_1985': historia_images_data.get('timeline_1985', {}).get('url', '/placeholder.svg?height=150&width=200'),
            'timeline_1995': historia_images_data.get('timeline_1995', {}).get('url', '/placeholder.svg?height=150&width=200'),
            'timeline_2010': historia_images_data.get('timeline_2010', {}).get('url', '/placeholder.svg?height=150&width=200'),
            'timeline_2024': historia_images_data.get('timeline_2024', {}).get('url', '/placeholder.svg?height=150&width=200'),
            'valores_image': historia_images_data.get('valores_image', {}).get('url', '/placeholder.svg?height=400&width=600')
        }
    except Exception as e:
        print(f"[v0] Error loading settings: {e}")
        hero_background_url = '/placeholder.svg?height=600&width=1200'
        historia_images = {
            'inicios_image': '/placeholder.svg?height=400&width=600',
            'timeline_1985': '/placeholder.svg?height=150&width=200',
            'timeline_1995': '/placeholder.svg?height=150&width=200',
            'timeline_2010': '/placeholder.svg?height=150&width=200',
            'timeline_2024': '/placeholder.svg?height=150&width=200',
            'valores_image': '/placeholder.svg?height=400&width=600'
        }
    
    return render_template('dashboard/admin.html', 
                         usuario=usuario, 
                         estadisticas=estadisticas,
                         fecha_actual=fecha_actual,
                         hero_background_url=hero_background_url,
                         historia_images=historia_images)

@dashboard_bp.route('/crear_empleado', methods=['POST'])
@admin_required
def crear_empleado():
    """Crear nuevo empleado"""
    try:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        cargo = request.form.get('cargo')
        telefono = request.form.get('telefono', '')
        password = request.form.get('password')
        
        # Validar datos
        if not all([nombre, email, cargo, password]):
            return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'})
        
        if cargo not in ['chef', 'vendedor']:
            return jsonify({'success': False, 'message': 'Cargo no válido'})
        
        # Verificar si el email ya existe
        if Usuario.find_by_email(email):
            return jsonify({'success': False, 'message': 'El email ya está registrado'})
        
        # Crear usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password,
            rol=cargo,
            telefono=telefono
        )
        
        if nuevo_usuario.save():
            return jsonify({
                'success': True, 
                'message': f'Empleado creado exitosamente con el cargo de {cargo}',
                'empleado': {
                    'nombre': nombre,
                    'email': email,
                    'cargo': cargo
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Error al crear el empleado'})
            
    except Exception as e:
        print(f"[v0] Error creando empleado: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'})

@dashboard_bp.route('/administrador')
@admin_required
def administrador():
    """Dashboard para administradores - redirige al dashboard admin"""
    return redirect(url_for('dashboard.admin'))

@dashboard_bp.route('/vendedor')
@role_required('vendedor')
def vendedor():
    """Dashboard para vendedores con funciones expandidas"""
    usuario = get_current_user()
    
    estadisticas = Venta.get_estadisticas()
    
    pedidos_pendientes = Venta.get_all(estado='pendiente')
    pedidos_preparando = Venta.get_all(estado='preparando')
    pedidos_listos = Venta.get_all(estado='listo')
    
    clientes_recientes = Cliente.get_all()[:10]
    
    from app.models.producto import Producto
    productos = Producto.get_all()[:5]
    
    total_usuarios = Usuario.count()
    total_clientes = len(Cliente.get_all())
    
    estadisticas.update({
        'total_usuarios': total_usuarios,
        'total_clientes': total_clientes,
        'pedidos_pendientes': len(pedidos_pendientes),
        'pedidos_preparando': len(pedidos_preparando),
        'pedidos_listos': len(pedidos_listos)
    })
    
    fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    def venta_to_tuple(venta):
        return (
            venta.id,           # 0 - ID
            venta.usuario_id,   # 1 - Usuario ID
            venta.total,        # 2 - Total
            venta.estado,       # 3 - Estado
            venta.fecha_pedido, # 4 - Fecha (corregido de fecha a fecha_pedido)
            venta.fecha_pedido.strftime('%d/%m/%Y %H:%M') if venta.fecha_pedido else '',  # 5 - Fecha formateada
            venta.direccion_entrega or 'Sin dirección',  # 6 - Dirección (corregido de direccion a direccion_entrega)
            venta.metodo_pago,  # 7 - Método de pago
            'Cliente'  # 8 - Nombre cliente (simplificado para evitar errores de relación)
        )
    
    pedidos_pendientes_tuplas = [venta_to_tuple(venta) for venta in pedidos_pendientes]
    pedidos_preparando_tuplas = [venta_to_tuple(venta) for venta in pedidos_preparando]
    pedidos_listos_tuplas = [venta_to_tuple(venta) for venta in pedidos_listos]
    
    return render_template('dashboard/vendedor.html', 
                         usuario=usuario, 
                         estadisticas=estadisticas,
                         pedidos_pendientes=pedidos_pendientes_tuplas,
                         pedidos_preparando=pedidos_preparando_tuplas,
                         pedidos_listos=pedidos_listos_tuplas,
                         clientes_recientes=clientes_recientes,
                         productos=productos,
                         fecha_actual=fecha_actual)

@dashboard_bp.route('/pedidos-nequi')
@role_required('vendedor')
def pedidos_nequi():
    """API para obtener pedidos con método de pago Nequi"""
    try:
        pedidos = Venta.get_pedidos_nequi()
        
        total = len(pedidos)
        sin_comprobante = sum(1 for p in pedidos if not p[11])  # comprobante_pago está en índice 11
        con_comprobante = total - sin_comprobante
        total_valor = sum(p[2] for p in pedidos)  # total está en índice 2
        
        pedidos_formateados = []
        for pedido in pedidos:
            fecha_str = pedido[4]  # fecha_pedido
            if fecha_str:
                try:
                    # Intentar parsear la fecha desde string
                    if '.' in fecha_str:
                        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')
                    else:
                        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                    fecha_formateada = fecha_obj.strftime('%d/%m/%Y %H:%M')
                except ValueError:
                    fecha_formateada = fecha_str  # Si no se puede parsear, usar el string original
            else:
                fecha_formateada = ''
            
            pedidos_formateados.append({
                'id': pedido[0],
                'usuario_id': pedido[1],
                'total': float(pedido[2]),
                'estado': pedido[3],
                'fecha_pedido': fecha_formateada,
                'direccion_entrega': pedido[5],
                'telefono_contacto': pedido[6],
                'notas': pedido[7],
                'metodo_pago': pedido[8],
                'fecha_entrega': pedido[9],
                'hora_entrega': pedido[10],
                'comprobante_pago': pedido[11],
                'cliente_nombre': pedido[12] or 'Cliente',
                'cliente_email': pedido[13] or ''
            })
        
        return jsonify({
            'success': True,
            'total': total,
            'sin_comprobante': sin_comprobante,
            'con_comprobante': con_comprobante,
            'total_valor': float(total_valor),
            'pedidos': pedidos_formateados
        })
        
    except Exception as e:
        print(f"[v0] Error obteniendo pedidos Nequi: {e}")
        return jsonify({'success': False, 'message': 'Error al obtener pedidos'})

@dashboard_bp.route('/subir-comprobante', methods=['POST'])
@role_required('vendedor')
def subir_comprobante():
    """Subir comprobante de pago para un pedido"""
    try:
        pedido_id = request.form.get('pedido_id')
        
        if 'comprobante' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
        
        file = request.files['comprobante']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
        
        if file and allowed_file(file.filename):
            # Crear directorio si no existe
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Generar nombre único para el archivo
            filename = secure_filename(f"comprobante_{pedido_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Guardar archivo
            file.save(filepath)
            
            # Actualizar base de datos
            venta = Venta.find_by_id(pedido_id)
            if venta:
                venta.update_comprobante(filepath)
                return jsonify({'success': True, 'message': 'Comprobante subido exitosamente'})
            else:
                return jsonify({'success': False, 'message': 'Pedido no encontrado'})
        
        return jsonify({'success': False, 'message': 'Tipo de archivo no permitido'})
        
    except Exception as e:
        print(f"[v0] Error subiendo comprobante: {e}")
        return jsonify({'success': False, 'message': 'Error al subir comprobante'})

@dashboard_bp.route('/ver-comprobante/<int:pedido_id>')
@role_required('vendedor')
def ver_comprobante(pedido_id):
    """Ver comprobante de pago de un pedido"""
    try:
        venta = Venta.find_by_id(pedido_id)
        if venta and venta.comprobante_pago:
            from flask import send_file
            return send_file(venta.comprobante_pago)
        else:
            return "Comprobante no encontrado", 404
            
    except Exception as e:
        print(f"[v0] Error mostrando comprobante: {e}")
        return "Error al mostrar comprobante", 500

@dashboard_bp.route('/chef')
@role_required('chef')
def chef():
    """Dashboard para chef/jefe de cocina"""
    usuario = get_current_user()
    insumos_bajo_stock = Insumo.get_low_stock()
    
    estadisticas = Venta.get_estadisticas()
    
    return render_template('dashboard/chef.html', 
                         usuario=usuario, 
                         insumos_bajo_stock=insumos_bajo_stock,
                         estadisticas=estadisticas)

@dashboard_bp.route('/actualizar_configuracion', methods=['POST'])
@admin_required
def actualizar_configuracion():
    """Actualizar configuraciones del sistema"""
    try:
        hero_background_url = request.form.get('hero_background_url')
        
        if not hero_background_url:
            return jsonify({'success': False, 'message': 'La URL de la imagen es requerida'})
        
        # Validar que sea una URL válida
        if not (hero_background_url.startswith('http://') or 
                hero_background_url.startswith('https://') or 
                hero_background_url.startswith('/')):
            return jsonify({'success': False, 'message': 'URL no válida. Debe comenzar con http://, https:// o /'})
        
        # Guardar configuración
        SystemSettings.set_setting('hero_background_url', hero_background_url, 
                                   'URL de la imagen de fondo del hero en la página de inicio')
        
        return jsonify({
            'success': True, 
            'message': 'Configuración actualizada exitosamente',
            'hero_background_url': hero_background_url
        })
        
    except Exception as e:
        print(f"[v0] Error actualizando configuración: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'})

@dashboard_bp.route('/actualizar_historia_images', methods=['POST'])
@admin_required
def actualizar_historia_images():
    """Actualizar imágenes de la página de historia"""
    try:
        from app.models.historia_images import HistoriaImages
        
        # Obtener todas las URLs del formulario
        image_keys = ['inicios_image', 'timeline_1985', 'timeline_1995', 
                     'timeline_2010', 'timeline_2024', 'valores_image']
        
        descriptions = {
            'inicios_image': 'Imagen de la sección Los Inicios',
            'timeline_1985': 'Imagen timeline 1985 - Los Primeros Pasos',
            'timeline_1995': 'Imagen timeline 1995 - Primera Expansión',
            'timeline_2010': 'Imagen timeline 2010 - Segunda Generación',
            'timeline_2024': 'Imagen timeline 2024 - Era Digital',
            'valores_image': 'Imagen de la sección Nuestros Valores'
        }
        
        updated_count = 0
        
        for key in image_keys:
            url = request.form.get(key)
            if url:
                # Validar que sea una URL válida
                if not (url.startswith('http://') or 
                       url.startswith('https://') or 
                       url.startswith('/')):
                    return jsonify({'success': False, 'message': f'URL no válida para {key}'})
                
                # Guardar la imagen
                HistoriaImages.set_image(key, url, descriptions.get(key, ''))
                updated_count += 1
        
        return jsonify({
            'success': True, 
            'message': f'{updated_count} imágenes actualizadas exitosamente'
        })
        
    except Exception as e:
        print(f"[v0] Error actualizando imágenes de historia: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'Error interno del servidor'})
