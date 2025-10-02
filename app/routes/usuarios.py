from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app.models.venta import Venta
from app.models.roles import Roles
from app.utils.decorators import admin_required
from datetime import datetime, timedelta
import calendar

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
@admin_required
def index():
    """Lista todos los usuarios"""
    usuarios = Usuario.get_all()
    return render_template('usuarios/index.html', usuarios=usuarios)

@usuarios_bp.route('/personal')
@admin_required
def personal():
    """Gestión de personal con estadísticas de ventas"""
    # Obtener fecha actual y del mes
    fecha_actual = datetime.now()
    primer_dia_mes = fecha_actual.replace(day=1)
    
    # Obtener vendedores y chefs activos
    vendedores = Usuario.get_by_role('vendedor')
    chefs = Usuario.get_by_role('chef')
    
    # Calcular estadísticas para vendedores
    for vendedor in vendedores:
        # Ventas del mes actual
        ventas_mes = Venta.get_ventas_by_vendedor_mes(vendedor.id, fecha_actual.year, fecha_actual.month)
        vendedor.ventas_mes = sum(venta.total for venta in ventas_mes)
        vendedor.pedidos_mes = len(ventas_mes)
    
    # Calcular estadísticas para chefs
    for chef in chefs:
        # Pedidos preparados en el mes
        pedidos_preparados = Venta.get_pedidos_preparados_by_chef_mes(chef.id, fecha_actual.year, fecha_actual.month)
        chef.pedidos_preparados_mes = len(pedidos_preparados)
    
    # Estadísticas generales
    total_vendedores = len([v for v in vendedores if v.activo])
    total_chefs = len([c for c in chefs if c.activo])
    ventas_mes_total = sum(v.ventas_mes for v in vendedores)
    pedidos_mes = sum(v.pedidos_mes for v in vendedores)
    
    return render_template('usuarios/personal.html',
                         vendedores=vendedores,
                         chefs=chefs,
                         total_vendedores=total_vendedores,
                         total_chefs=total_chefs,
                         ventas_mes_total=ventas_mes_total,
                         pedidos_mes=pedidos_mes)

@usuarios_bp.route('/crear', methods=['GET', 'POST'])
@admin_required
def crear():
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        telefono = request.form.get('telefono', '')
        direccion = request.form.get('direccion', '')
        rol = request.form['rol']
        
        # Validaciones
        if not all([nombre, email, password, rol]):
            flash('Por favor completa todos los campos obligatorios', 'error')
            return render_template('usuarios/crear.html', roles=['vendedor', 'chef', 'cliente', 'admin'])
        
        roles_permitidos = ['vendedor', 'chef', 'cliente', 'admin']
        if rol not in roles_permitidos:
            flash('Rol inválido', 'error')
            return render_template('usuarios/crear.html', roles=roles_permitidos)
        
        if Usuario.find_by_email(email):
            flash('Este email ya está registrado', 'error')
            return render_template('usuarios/crear.html', roles=roles_permitidos)
        
        try:
            Usuario.create({
                'nombre': nombre,
                'email': email,
                'password': password,
                'telefono': telefono,
                'direccion': direccion,
                'rol': rol
            })
            
            flash('Usuario creado exitosamente', 'success')
            if request.referrer and 'personal' in request.referrer:
                return redirect(url_for('usuarios.personal'))
            return redirect(url_for('usuarios.index'))
            
        except Exception as e:
            flash('Error al crear el usuario', 'error')
    
    return render_template('usuarios/crear.html', roles=['vendedor', 'chef', 'cliente', 'admin'])

@usuarios_bp.route('/<int:usuario_id>')
@admin_required
def detalle(usuario_id):
    """Ver detalles de un usuario"""
    usuario = Usuario.find_by_id(usuario_id)
    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.index'))
    
    rol_descripcion = Roles.get_descripcion_rol(usuario.rol)
    permisos = Roles.get_permisos_rol(usuario.rol)
    
    return render_template('usuarios/detalle.html', 
                         usuario=usuario,
                         rol_descripcion=rol_descripcion,
                         permisos=permisos)

@usuarios_bp.route('/<int:usuario_id>/editar', methods=['GET', 'POST'])
@admin_required
def editar(usuario_id):
    """Editar un usuario"""
    usuario = Usuario.find_by_id(usuario_id)
    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.index'))
    
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'telefono': request.form.get('telefono', ''),
            'direccion': request.form.get('direccion', ''),
            'rol': request.form['rol']
        }
        
        # Verificar email único (excepto el actual)
        existing_user = Usuario.find_by_email(data['email'])
        if existing_user and existing_user.id != usuario_id:
            flash('Este email ya está en uso por otro usuario', 'error')
            return render_template('usuarios/editar.html', 
                                 usuario=usuario, 
                                 roles=['vendedor', 'chef', 'cliente', 'admin'])
        
        # Verificar rol válido
        if data['rol'] not in ['vendedor', 'chef', 'cliente', 'admin']:
            flash('Rol inválido', 'error')
            return render_template('usuarios/editar.html', 
                                 usuario=usuario, 
                                 roles=['vendedor', 'chef', 'cliente', 'admin'])
        
        try:
            usuario.update(data)
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios.detalle', usuario_id=usuario_id))
            
        except Exception as e:
            flash('Error al actualizar el usuario', 'error')
    
    return render_template('usuarios/editar.html', 
                         usuario=usuario, 
                         roles=['vendedor', 'chef', 'cliente', 'admin'])
