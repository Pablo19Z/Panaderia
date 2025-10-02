from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from app.models.usuario import Usuario
from app.models.roles import Roles

class UsuarioForm(FlaskForm):
    """Formulario para crear/editar usuarios (admin)"""
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres')
    ], render_kw={'placeholder': 'Nombre completo del usuario', 'class': 'form-control'})
    
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingresa un email válido')
    ], render_kw={'placeholder': 'usuario@email.com', 'class': 'form-control'})
    
    password = PasswordField('Contraseña', validators=[
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ], render_kw={'placeholder': 'Dejar vacío para mantener actual', 'class': 'form-control'})
    
    telefono = StringField('Teléfono', validators=[
        Length(max=20, message='El teléfono no puede exceder 20 caracteres')
    ], render_kw={'placeholder': '+1 234 567 8900', 'class': 'form-control'})
    
    direccion = TextAreaField('Dirección', validators=[
        Length(max=200, message='La dirección no puede exceder 200 caracteres')
    ], render_kw={'placeholder': 'Dirección del usuario', 'class': 'form-control', 'rows': 3})
    
    rol = SelectField('Rol', validators=[
        DataRequired(message='Selecciona un rol')
    ], render_kw={'class': 'form-select'})
    
    activo = BooleanField('Usuario Activo', default=True, render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Guardar Usuario', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, usuario_id=None, is_edit=False, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.usuario_id = usuario_id
        self.is_edit = is_edit
        
        # Cargar roles disponibles
        roles = Roles.get_roles_disponibles()
        self.rol.choices = [(rol, Roles.get_descripcion_rol(rol)) for rol in roles]
        
        # Si es edición, la contraseña es opcional
        if is_edit:
            self.password.validators = [Optional(), Length(min=6, message='La contraseña debe tener al menos 6 caracteres')]
    
    def validate_email(self, email):
        """Validar que el email no esté ya registrado por otro usuario"""
        usuario = Usuario.find_by_email(email.data)
        if usuario and (not self.usuario_id or usuario.id != self.usuario_id):
            raise ValidationError('Este email ya está registrado')
    
    def validate_password(self, password):
        """Validar contraseña solo si es requerida"""
        if not self.is_edit and not password.data:
            raise ValidationError('La contraseña es obligatoria para nuevos usuarios')

class CambiarRolForm(FlaskForm):
    """Formulario rápido para cambiar rol de usuario"""
    rol = SelectField('Nuevo Rol', validators=[
        DataRequired(message='Selecciona un rol')
    ], render_kw={'class': 'form-select'})
    
    submit = SubmitField('Cambiar Rol', render_kw={'class': 'btn btn-warning'})
    
    def __init__(self, *args, **kwargs):
        super(CambiarRolForm, self).__init__(*args, **kwargs)
        roles = Roles.get_roles_disponibles()
        self.rol.choices = [(rol, rol.title()) for rol in roles]
