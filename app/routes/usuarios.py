from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app.models.roles import Roles
from app.utils.decorators import admin_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/')
@admin_required
def index():
    """Lista todos los usuarios"""
    usuarios = Usuario.get_all()
    return render_template('usuarios/index.html', usuarios=usuarios)

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
            return render_template('usuarios/crear.html', roles=Roles.get_roles_disponibles())
        
        if rol not in Roles.get_roles_disponibles():
            flash('Rol inválido', 'error')
            return render_template('usuarios/crear.html', roles=Roles.get_roles_disponibles())
        
        if Usuario.find_by_email(email):
            flash('Este email ya está registrado', 'error')
            return render_template('usuarios/crear.html', roles=Roles.get_roles_disponibles())
        
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
            return redirect(url_for('usuarios.index'))
            
        except Exception as e:
            flash('Error al crear el usuario', 'error')
    
    return render_template('usuarios/crear.html', roles=Roles.get_roles_disponibles())

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
                                 roles=Roles.get_roles_disponibles())
        
        # Verificar rol válido
        if data['rol'] not in Roles.get_roles_disponibles():
            flash('Rol inválido', 'error')
            return render_template('usuarios/editar.html', 
                                 usuario=usuario, 
                                 roles=Roles.get_roles_disponibles())
        
        try:
            usuario.update(data)
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios.detalle', usuario_id=usuario_id))
            
        except Exception as e:
            flash('Error al actualizar el usuario', 'error')
    
    return render_template('usuarios/editar.html', 
                         usuario=usuario, 
                         roles=Roles.get_roles_disponibles())
