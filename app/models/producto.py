from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio_min = db.Column(db.Float, nullable=False)
    precio_max = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    imagen = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)  # Nuevo campo para inventario
    categoria = db.relationship('Categoria', backref='productos', lazy=True)

    def __repr__(self):
        return f'<Producto {self.nombre}>'