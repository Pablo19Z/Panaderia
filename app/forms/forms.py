from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')