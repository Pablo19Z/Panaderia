from app import db
import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(80), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    cargo = db.Column(db.String(100))
    salario = db.Column(db.DECIMAL(10, 2))
    fecha_ingreso = db.Column(db.Date, default=datetime.date.today)

    rol = db.relationship('Rol', backref='usuarios')

    def __repr__(self):
        return str(self.id)