from app import db

class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio_min = db.Column(db.DECIMAL(10, 2), nullable=False)
    precio_max = db.Column(db.DECIMAL(10, 2), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    imagen = db.Column(db.String(200))
    stock = db.Column(db.Integer, nullable=False)

    # Relación con Categoria
    categoria = db.relationship('Categoria', backref='productos')

    def __repr__(self):
        return f'<Producto {self.nombre}>'