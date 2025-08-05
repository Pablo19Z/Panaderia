from app import db

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    total = db.Column(db.DECIMAL(10, 2), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)