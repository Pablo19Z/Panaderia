# app/models/usuario.py
from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    cargo = db.Column(db.String(100))
    salario = db.Column(db.DECIMAL(10, 2))
    fecha_ingreso = db.Column(db.Date, nullable=False)

    # Relación con Rol
    rol = db.relationship('Rol', backref='usuarios')

    def __repr__(self):
        return f'<Usuario {self.nombre}>'