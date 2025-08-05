from app import db

class ClienteProducto(db.Model):
    __tablename__ = 'cliente_producto'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    subtotal = db.Column(db.DECIMAL(10, 2), nullable=False)

    # Relación con Cliente usando back_populates
    cliente = db.relationship('Cliente', back_populates='carrito')
    # Relación con Producto usando backref (puedes cambiar a back_populates si prefieres)
    producto = db.relationship('Producto', backref='en_carrito')

    def __repr__(self):
        return f'<ClienteProducto {self.cliente_id}, {self.producto_id}>'