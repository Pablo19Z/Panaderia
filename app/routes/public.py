from flask import render_template, redirect, url_for, flash, session, request
from app import db
from app.models import Producto, Cliente, ClienteProducto
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        cliente = Cliente(nombre=form.nombre.data, email=form.email.data)
        cliente.set_password(form.contraseña.data)
        try:
            db.session.add(cliente)
            db.session.commit()
            flash('¡Registro exitoso! Por favor, inicia sesión para disfrutar de nuestros panes.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Este correo ya está registrado. Usa otro o inicia sesión.', 'danger')
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
        flash('Inicio de sesión fallido. Verifica tu email y contraseña.', 'danger')
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

def logout():
    logout_user()
    flash('¡Has cerrado sesión con éxito! Vuelve pronto por más delicias.', 'success')
    return redirect(url_for('index'))

def add_to_cart(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form.get('cantidad', 1))
    categoria_nombre = producto.categoria.nombre.lower() if producto.categoria else 'producto'
    if cantidad > producto.stock:
        flash('La cantidad solicitada excede el stock disponible.', 'danger')
        return redirect(url_for('index'))
    if cantidad > 0:
        if current_user.is_authenticated:
            carrito = current_user.carrito
            existing_item = next((item for item in carrito if item.producto_id == producto_id), None)
            if existing_item:
                if producto.stock >= cantidad:
                    existing_item.cantidad += cantidad
                    existing_item.subtotal = existing_item.cantidad * producto.precio_min
                    producto.stock -= cantidad
                    db.session.commit()
                    item_type = 'panes' if categoria_nombre == 'panes' else 'pasteles' if categoria_nombre == 'pasteles' else 'dulces'
                    flash(f'¡{existing_item.cantidad} {item_type} recién horneados añadidos a tu carrito!', 'success')
                else:
                    flash('No hay suficiente stock disponible.', 'danger')
            else:
                item = ClienteProducto(cliente_id=current_user.id, producto_id=producto_id, cantidad=cantidad, subtotal=cantidad * producto.precio_min)
                db.session.add(item)
                producto.stock -= cantidad
                db.session.commit()
                item_type = 'pan' if categoria_nombre == 'panes' else 'pastel' if categoria_nombre == 'pasteles' else 'dulce'
                flash(f'¡{cantidad} {item_type} recién horneado/a añadido a tu carrito!', 'success')
        else:
            if str(producto_id) not in session.get('cart', {}):
                session['cart'] = session.get('cart', {})
                session['cart'][str(producto_id)] = cantidad
                item_type = 'dulce' if categoria_nombre == 'galletas' else 'pan' if categoria_nombre == 'panes' else 'pastel' if categoria_nombre == 'pasteles' else 'producto'
                flash(f'¡{cantidad} {item_type} añadido a tu carrito temporal! Inicia sesión para guardarlo.', 'info')
            else:
                if producto.stock >= session['cart'][str(producto_id)] + cantidad:
                    session['cart'][str(producto_id)] += cantidad
                    item_type = 'dulces' if categoria_nombre == 'galletas' else 'panes' if categoria_nombre == 'panes' else 'pasteles' if categoria_nombre == 'pasteles' else 'productos'
                    flash(f'¡{session["cart"][str(producto_id)]} {item_type} añadidos a tu carrito temporal! Inicia sesión para guardarlo.', 'info')
                else:
                    flash('No hay suficiente stock disponible.', 'danger')
            session.modified = True
    else:
        flash('La cantidad debe ser mayor que 0.', 'danger')
    return redirect(url_for('cart'))

def clear_cart():
    if current_user.is_authenticated:
        carrito = current_user.carrito
        for item in carrito:
            producto = Producto.query.get(item.producto_id)
            if producto:
                producto.stock += item.cantidad
                db.session.delete(item)
        db.session.commit()
        flash('¡Tu carrito ha sido vaciado! Los panes y dulces han vuelto al mostrador.', 'success')
    else:
        if 'cart' in session:
            for prod_id, qty in session['cart'].items():
                producto = Producto.query.get(prod_id)
                if producto:
                    producto.stock += qty
            session.pop('cart', None)
            flash('¡Tu carrito temporal ha sido vaciado! Los panes han vuelto al mostrador.', 'info')
    return redirect(url_for('cart'))

def cart():
    carrito = []
    total = 0
    if current_user.is_authenticated:
        carrito = current_user.carrito
        total = sum(item.subtotal for item in carrito) if carrito else 0
    else:
        cart_data = session.get('cart', {})
        for prod_id, qty in cart_data.items():
            producto = Producto.query.get(prod_id)
            if producto:
                carrito.append({'producto': producto, 'cantidad': qty, 'subtotal': producto.precio_min * qty})
                total += producto.precio_min * qty
    return render_template('cart/index.html', carrito=carrito, total=total if total > 0 else None)

def index():
    productos = Producto.query.all()
    return render_template('productos/index.html', productos=productos)