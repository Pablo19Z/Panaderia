from app import db

class Insumo(db.Model):
    __tablename__ = 'insumos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad_medida = db.Column(db.String(20))
    stock_actual = db.Column(db.DECIMAL(10, 2), default=0)