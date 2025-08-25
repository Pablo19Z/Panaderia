from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from app.models.categoria import Categoria

class ProductoForm(FlaskForm):
    """Formulario para crear/editar productos"""
    nombre = StringField('Nombre del Producto', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres')
    ], render_kw={'placeholder': 'Ej: Pan Francés Artesanal', 'class': 'form-control'})
    
    descripcion = TextAreaField('Descripción', validators=[
        Length(max=500, message='La descripción no puede exceder 500 caracteres')
    ], render_kw={'placeholder': 'Describe el producto, ingredientes especiales, etc.', 'class': 'form-control', 'rows': 4})
    
    precio = DecimalField('Precio ($)', validators=[
        DataRequired(message='El precio es obligatorio'),
        NumberRange(min=0.01, message='El precio debe ser mayor a 0')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    categoria_id = SelectField('Categoría', validators=[
        DataRequired(message='Selecciona una categoría')
    ], coerce=int, render_kw={'class': 'form-select'})
    
    stock = IntegerField('Stock Inicial', validators=[
        DataRequired(message='El stock es obligatorio'),
        NumberRange(min=0, message='El stock no puede ser negativo')
    ], render_kw={'placeholder': '0', 'class': 'form-control'})
    
    imagen = FileField('Imagen del Producto', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes (JPG, PNG, GIF)')
    ], render_kw={'class': 'form-control', 'accept': 'image/*'})
    
    activo = BooleanField('Producto Activo', default=True, render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('Guardar Producto', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Cargar categorías dinámicamente
        categorias = Categoria.get_all()
        self.categoria_id.choices = [(0, 'Selecciona una categoría')] + [(c.id, c.nombre) for c in categorias]

class BuscarProductoForm(FlaskForm):
    """Formulario de búsqueda de productos"""
    q = StringField('Buscar productos...', validators=[
        Length(max=100, message='La búsqueda no puede exceder 100 caracteres')
    ], render_kw={'placeholder': 'Buscar por nombre o descripción', 'class': 'form-control'})
    
    categoria = SelectField('Categoría', coerce=int, render_kw={'class': 'form-select'})
    
    submit = SubmitField('Buscar', render_kw={'class': 'btn btn-outline-primary'})
    
    def __init__(self, *args, **kwargs):
        super(BuscarProductoForm, self).__init__(*args, **kwargs)
        categorias = Categoria.get_all()
        self.categoria.choices = [(0, 'Todas las categorías')] + [(c.id, c.nombre) for c in categorias]
