from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models.insumo import Insumo

class InsumoForm(FlaskForm):
    """Formulario para crear/editar insumos"""
    nombre = StringField('Nombre del Insumo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=2, max=100, message='El nombre debe tener entre 2 y 100 caracteres')
    ], render_kw={'placeholder': 'Ej: Harina de Trigo', 'class': 'form-control'})
    
    descripcion = TextAreaField('Descripción', validators=[
        Length(max=300, message='La descripción no puede exceder 300 caracteres')
    ], render_kw={'placeholder': 'Descripción del insumo, características especiales...', 'class': 'form-control', 'rows': 3})
    
    cantidad_actual = DecimalField('Cantidad Actual', validators=[
        DataRequired(message='La cantidad actual es obligatoria'),
        NumberRange(min=0, message='La cantidad no puede ser negativa')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    cantidad_minima = DecimalField('Cantidad Mínima (Alerta)', validators=[
        DataRequired(message='La cantidad mínima es obligatoria'),
        NumberRange(min=0, message='La cantidad no puede ser negativa')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    unidad_medida = SelectField('Unidad de Medida', validators=[
        DataRequired(message='Selecciona una unidad de medida')
    ], choices=[
        ('kg', 'Kilogramos (kg)'),
        ('g', 'Gramos (g)'),
        ('l', 'Litros (l)'),
        ('ml', 'Mililitros (ml)'),
        ('unidades', 'Unidades'),
        ('cajas', 'Cajas'),
        ('paquetes', 'Paquetes')
    ], render_kw={'class': 'form-select'})
    
    precio_compra = DecimalField('Precio de Compra por Unidad', validators=[
        NumberRange(min=0, message='El precio no puede ser negativo')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    proveedor = StringField('Proveedor', validators=[
        Length(max=100, message='El proveedor no puede exceder 100 caracteres')
    ], render_kw={'placeholder': 'Nombre del proveedor', 'class': 'form-control'})
    
    submit = SubmitField('Guardar Insumo', render_kw={'class': 'btn btn-primary'})

class MovimientoInventarioForm(FlaskForm):
    """Formulario para registrar movimientos de inventario"""
    insumo_id = SelectField('Insumo', validators=[
        DataRequired(message='Selecciona un insumo')
    ], coerce=int, render_kw={'class': 'form-select'})
    
    tipo_movimiento = SelectField('Tipo de Movimiento', validators=[
        DataRequired(message='Selecciona el tipo de movimiento')
    ], choices=[
        ('entrada', 'Entrada (Agregar stock)'),
        ('salida', 'Salida (Reducir stock)')
    ], render_kw={'class': 'form-select'})
    
    cantidad = DecimalField('Cantidad', validators=[
        DataRequired(message='La cantidad es obligatoria'),
        NumberRange(min=0.01, message='La cantidad debe ser mayor a 0')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    motivo = TextAreaField('Motivo del Movimiento', validators=[
        DataRequired(message='El motivo es obligatorio'),
        Length(min=5, max=200, message='El motivo debe tener entre 5 y 200 caracteres')
    ], render_kw={'placeholder': 'Describe el motivo del movimiento (compra, uso en producción, merma, etc.)', 'class': 'form-control', 'rows': 3})
    
    submit = SubmitField('Registrar Movimiento', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, *args, **kwargs):
        super(MovimientoInventarioForm, self).__init__(*args, **kwargs)
        # Cargar insumos disponibles
        insumos = Insumo.get_all()
        self.insumo_id.choices = [(0, 'Selecciona un insumo')] + [(i.id, f"{i.nombre} ({i.cantidad_actual} {i.unidad_medida})") for i in insumos]

class EntradaInventarioForm(FlaskForm):
    """Formulario específico para entradas de inventario"""
    insumo_id = SelectField('Insumo', validators=[
        DataRequired(message='Selecciona un insumo')
    ], coerce=int, render_kw={'class': 'form-select'})
    
    cantidad = DecimalField('Cantidad a Ingresar', validators=[
        DataRequired(message='La cantidad es obligatoria'),
        NumberRange(min=0.01, message='La cantidad debe ser mayor a 0')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    motivo = TextAreaField('Motivo de la Entrada', validators=[
        DataRequired(message='El motivo es obligatorio'),
        Length(min=5, max=200, message='El motivo debe tener entre 5 y 200 caracteres')
    ], render_kw={'placeholder': 'Ej: Compra a proveedor, devolución, ajuste de inventario...', 'class': 'form-control', 'rows': 3})
    
    submit = SubmitField('Registrar Entrada', render_kw={'class': 'btn btn-success'})
    
    def __init__(self, *args, **kwargs):
        super(EntradaInventarioForm, self).__init__(*args, **kwargs)
        insumos = Insumo.get_all()
        self.insumo_id.choices = [(0, 'Selecciona un insumo')] + [(i.id, f"{i.nombre} (Stock actual: {i.cantidad_actual} {i.unidad_medida})") for i in insumos]

class SalidaInventarioForm(FlaskForm):
    """Formulario específico para salidas de inventario"""
    insumo_id = SelectField('Insumo', validators=[
        DataRequired(message='Selecciona un insumo')
    ], coerce=int, render_kw={'class': 'form-select'})
    
    cantidad = DecimalField('Cantidad a Retirar', validators=[
        DataRequired(message='La cantidad es obligatoria'),
        NumberRange(min=0.01, message='La cantidad debe ser mayor a 0')
    ], render_kw={'placeholder': '0.00', 'class': 'form-control', 'step': '0.01'})
    
    motivo = TextAreaField('Motivo de la Salida', validators=[
        DataRequired(message='El motivo es obligatorio'),
        Length(min=5, max=200, message='El motivo debe tener entre 5 y 200 caracteres')
    ], render_kw={'placeholder': 'Ej: Uso en producción, merma, venta directa...', 'class': 'form-control', 'rows': 3})
    
    submit = SubmitField('Registrar Salida', render_kw={'class': 'btn btn-danger'})
    
    def __init__(self, *args, **kwargs):
        super(SalidaInventarioForm, self).__init__(*args, **kwargs)
        insumos = Insumo.get_all()
        self.insumo_id.choices = [(0, 'Selecciona un insumo')] + [(i.id, f"{i.nombre} (Disponible: {i.cantidad_actual} {i.unidad_medida})") for i in insumos]
