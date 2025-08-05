from app import db

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.DECIMAL(10, 2))
    subtotal = db.Column(db.DECIMAL(10, 2))