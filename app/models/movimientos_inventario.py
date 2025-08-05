from app import db

class MovimientosInventario(db.Model):
    __tablename__ = 'movimientos_inventario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.Enum('entrada', 'salida'), nullable=False)
    cantidad = db.Column(db.DECIMAL(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    descripcion = db.Column(db.Text)