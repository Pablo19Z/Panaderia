from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models.usuario import Usuario

class ClienteForm(FlaskForm):
    """Formulario para crear/editar clientes"""
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres')
    ], render_kw={'placeholder': 'Nombre completo del cliente', 'class': 'form-control'})
    
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingresa un email válido')
    ], render_kw={'placeholder': 'cliente@email.com', 'class': 'form-control'})
    
    telefono = StringField('Teléfono', validators=[
        Length(max=20, message='El teléfono no puede exceder 20 caracteres')
    ], render_kw={'placeholder': '+1 234 567 8900', 'class': 'form-control'})
    
    direccion = TextAreaField('Dirección', validators=[
        Length(max=200, message='La dirección no puede exceder 200 caracteres')
    ], render_kw={'placeholder': 'Dirección completa del cliente', 'class': 'form-control', 'rows': 3})
    
    submit = SubmitField('Guardar Cliente', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, cliente_id=None, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.cliente_id = cliente_id
    
    def validate_email(self, email):
        """Validar que el email no esté ya registrado por otro cliente"""
        usuario = Usuario.find_by_email(email.data)
        if usuario and (not self.cliente_id or usuario.id != self.cliente_id):
            raise ValidationError('Este email ya está registrado')

class CheckoutForm(FlaskForm):
    """Formulario de checkout/pago"""
    direccion_entrega = TextAreaField('Dirección de Entrega', validators=[
        DataRequired(message='La dirección de entrega es obligatoria'),
        Length(min=10, max=200, message='La dirección debe tener entre 10 y 200 caracteres')
    ], render_kw={'placeholder': 'Dirección completa donde entregar el pedido', 'class': 'form-control', 'rows': 3})
    
    telefono_contacto = StringField('Teléfono de Contacto', validators=[
        DataRequired(message='El teléfono de contacto es obligatorio'),
        Length(min=8, max=20, message='El teléfono debe tener entre 8 y 20 caracteres')
    ], render_kw={'placeholder': '+1 234 567 8900', 'class': 'form-control'})
    
    notas = TextAreaField('Notas Especiales', validators=[
        Length(max=300, message='Las notas no pueden exceder 300 caracteres')
    ], render_kw={'placeholder': 'Instrucciones especiales para la entrega (opcional)', 'class': 'form-control', 'rows': 3})
    
    metodo_pago = SelectField('Método de Pago', validators=[
        DataRequired(message='Selecciona un método de pago')
    ], choices=[
        ('efectivo', 'Efectivo al entregar'),
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('transferencia', 'Transferencia bancaria')
    ], render_kw={'class': 'form-select'})
    
    submit = SubmitField('Confirmar Pedido', render_kw={'class': 'btn btn-success btn-lg w-100'})

class ResenaForm(FlaskForm):
    """Formulario para escribir reseñas"""
    calificacion = SelectField('Calificación', validators=[
        DataRequired(message='Selecciona una calificación')
    ], choices=[
        (5, '⭐⭐⭐⭐⭐ Excelente'),
        (4, '⭐⭐⭐⭐ Muy bueno'),
        (3, '⭐⭐⭐ Bueno'),
        (2, '⭐⭐ Regular'),
        (1, '⭐ Malo')
    ], coerce=int, render_kw={'class': 'form-select'})
    
    comentario = TextAreaField('Comentario', validators=[
        Length(max=500, message='El comentario no puede exceder 500 caracteres')
    ], render_kw={'placeholder': 'Comparte tu experiencia con este producto...', 'class': 'form-control', 'rows': 4})
    
    submit = SubmitField('Publicar Reseña', render_kw={'class': 'btn btn-primary'})
