from functools import wraps
from flask import session, redirect, url_for, flash, request
import hashlib

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """Decorador para requerir un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            if session.get('user_role') != required_role:
                flash('No tienes permisos para acceder a esta página.', 'error')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        user_role = session.get('user_role')
        if user_role not in ['admin', 'administrador']:
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_or_vendedor_required(f):
    """Decorador para requerir rol de administrador o vendedor"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        user_role = session.get('user_role')
        if user_role not in ['admin', 'administrador', 'vendedor']:
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Función para hashear contraseñas"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Función para verificar contraseñas"""
    return hash_password(password) == hashed

def format_currency(amount):
    """Formatear cantidad como moneda"""
    return f"${amount:.2f}"

def calculate_total_with_tax(subtotal, tax_rate=0.12):
    """Calcular total con impuestos"""
    tax = subtotal * tax_rate
    return subtotal + tax
