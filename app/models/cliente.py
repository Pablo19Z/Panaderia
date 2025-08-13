from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    descuento_primer = db.Column(db.Float, default=0.0)
    contrasenia_hash = db.Column(db.String(128))

    # Relación con ClienteProducto usando back_populates
    carrito = db.relationship('ClienteProducto', back_populates='cliente', lazy=True)

    # Métodos
    def set_password(self, password):
        self.contrasenia_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasenia_hash, password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'<Cliente {self.nombre}>'