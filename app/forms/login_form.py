from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models.usuario import Usuario

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingresa un email válido')
    ], render_kw={'placeholder': 'tu@email.com', 'class': 'form-control'})
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ], render_kw={'placeholder': 'Tu contraseña', 'class': 'form-control'})
    
    remember_me = BooleanField('Recordarme', render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Iniciar Sesión', render_kw={'class': 'btn btn-primary w-100'})
    
    def validate_email(self, email):
        """Validar que el email existe y está activo"""
        usuario = Usuario.find_by_email(email.data)
        if not usuario:
            raise ValidationError('Email no registrado')
        if not usuario.activo:
            raise ValidationError('Cuenta desactivada')

class RegisterForm(FlaskForm):
    """Formulario de registro de usuarios"""
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres')
    ], render_kw={'placeholder': 'Tu nombre completo', 'class': 'form-control'})
    
    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingresa un email válido')
    ], render_kw={'placeholder': 'tu@email.com', 'class': 'form-control'})
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ], render_kw={'placeholder': 'Mínimo 6 caracteres', 'class': 'form-control'})
    
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Confirma tu contraseña')
    ], render_kw={'placeholder': 'Repite tu contraseña', 'class': 'form-control'})
    
    telefono = StringField('Teléfono', validators=[
        Length(max=20, message='El teléfono no puede exceder 20 caracteres')
    ], render_kw={'placeholder': '+1 234 567 8900', 'class': 'form-control'})
    
    direccion = StringField('Dirección', validators=[
        Length(max=200, message='La dirección no puede exceder 200 caracteres')
    ], render_kw={'placeholder': 'Tu dirección completa', 'class': 'form-control'})
    
    submit = SubmitField('Crear Cuenta', render_kw={'class': 'btn btn-primary w-100'})
    
    def validate_email(self, email):
        """Validar que el email no esté ya registrado"""
        usuario = Usuario.find_by_email(email.data)
        if usuario:
            raise ValidationError('Este email ya está registrado')
    
    def validate_confirm_password(self, confirm_password):
        """Validar que las contraseñas coincidan"""
        if self.password.data != confirm_password.data:
            raise ValidationError('Las contraseñas no coinciden')

class ChangePasswordForm(FlaskForm):
    """Formulario para cambiar contraseña"""
    current_password = PasswordField('Contraseña Actual', validators=[
        DataRequired(message='Ingresa tu contraseña actual')
    ], render_kw={'class': 'form-control'})
    
    new_password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message='La nueva contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ], render_kw={'class': 'form-control'})
    
    confirm_new_password = PasswordField('Confirmar Nueva Contraseña', validators=[
        DataRequired(message='Confirma tu nueva contraseña')
    ], render_kw={'class': 'form-control'})
    
    submit = SubmitField('Cambiar Contraseña', render_kw={'class': 'btn btn-primary'})
    
    def validate_confirm_new_password(self, confirm_new_password):
        """Validar que las nuevas contraseñas coincidan"""
        if self.new_password.data != confirm_new_password.data:
            raise ValidationError('Las contraseñas no coinciden')
