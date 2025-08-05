from flask import render_template, redirect, url_for, flash, abort
from app import db
from app.models import Producto, Cliente, ClienteProducto
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        cliente = Cliente(nombre=form.nombre.data, email=form.email.data)
        cliente.set_password(form.contraseña.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Registro exitoso! Por favor inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Registro', form=form)

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()
        if cliente and cliente.check_password(form.contraseña.data):
            login_user(cliente)
            return redirect(url_for('index'))
        flash('Login fallido. Verifica tu email y contraseña.', 'danger')
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required  # Requiere autenticación para agregar al carrito
def add_to_cart(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    if producto.stock > 0:
        carrito = current_user.carrito
        if not any(item.producto_id == producto_id for item in carrito):
            item = ClienteProducto(cliente_id=current_user.id, producto_id=producto_id, cantidad=1, subtotal=producto.precio_min)
            db.session.add(item)
            producto.stock -= 1
            db.session.commit()
            flash('Producto agregado al carrito!', 'success')
        else:
            flash('Este producto ya está en tu carrito.', 'warning')
    else:
        flash('No hay stock disponible.', 'danger')
    return redirect(url_for('index'))

@login_required  # Requiere autenticación para ver el carrito
def cart():
    carrito = current_user.carrito
    total = sum(item.subtotal for item in carrito)
    return render_template('cart/index.html', carrito=carrito, total=total)

def index():
    productos = Producto.query.all()
    return render_template('productos/index.html', productos=productos)