from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import Cliente

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('contraseña', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrarse')

    def validate_email(self, email):
        user = Cliente.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El correo ya está registrado.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')