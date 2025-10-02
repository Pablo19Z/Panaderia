from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Por favor completa todos los campos', 'error')
            return render_template('auth/login.html')
        
        usuario = Usuario.find_by_email(email)
        
        if usuario and usuario.verify_password(password):
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombre
            session['user_role'] = usuario.rol
            flash(f'¡Bienvenido {usuario.nombre}!', 'success')
            
            # Redirigir según el rol
            if usuario.rol == 'admin':
                return redirect(url_for('dashboard.admin'))
            elif usuario.rol == 'vendedor':
                return redirect(url_for('dashboard.vendedor'))
            elif usuario.rol == 'chef':
                return redirect(url_for('dashboard.chef'))
            else:
                return redirect(url_for('dashboard.cliente'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuarios"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        telefono = request.form.get('telefono', '')
        direccion = request.form.get('direccion', '')
        
        # Validaciones
        if not all([nombre, email, password, confirm_password]):
            flash('Por favor completa todos los campos obligatorios', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('auth/register.html')
        
        # Verificar si el email ya existe
        if Usuario.find_by_email(email):
            flash('Este email ya está registrado', 'error')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        try:
            user_id = Usuario.create({
                'nombre': nombre,
                'email': email,
                'password': password,
                'telefono': telefono,
                'direccion': direccion,
                'rol': 'cliente'
            })
            
            # Iniciar sesión automáticamente
            session['user_id'] = user_id
            session['user_name'] = nombre
            session['user_role'] = 'cliente'
            
            flash('¡Registro exitoso! Bienvenido a Migas de oro Dorè', 'success')
            return redirect(url_for('dashboard.cliente'))
            
        except Exception as e:
            flash('Error al crear la cuenta. Intenta nuevamente.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))
