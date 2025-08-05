from .public import index, register, login, logout, add_to_cart, cart

def register_routes(app):
    app.route('/')(index)
    app.route('/register', methods=['GET', 'POST'])(register)
    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout')(logout)
    app.route('/add_to_cart/<int:producto_id>', methods=['POST'])(add_to_cart)
    app.route('/cart')(cart)  # Nueva ruta para el carrito