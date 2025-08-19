from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.insumo import Insumo
from app.models.movimientos_inventario import MovimientoInventario
from app.utils.decorators import login_required, role_required
from datetime import datetime

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@inventario_bp.route('/')
@role_required('chef')
def index():
    """Lista todos los insumos del inventario"""
    insumos = Insumo.get_all()
    insumos_bajo_stock = Insumo.get_low_stock()
    
    return render_template('inventario/index.html', 
                         insumos=insumos,
                         insumos_bajo_stock=insumos_bajo_stock)

@inventario_bp.route('/<int:insumo_id>')
@role_required('chef')
def detalle(insumo_id):
    """Ver detalles de un insumo"""
    insumo = Insumo.find_by_id(insumo_id)
    if not insumo:
        flash('Insumo no encontrado', 'error')
        return redirect(url_for('inventario.index'))
    
    # Obtener movimientos recientes del insumo
    movimientos = MovimientoInventario.get_all(insumo_id=insumo_id, limit=20)
    
    return render_template('inventario/detalle.html', 
                         insumo=insumo,
                         movimientos=movimientos)

@inventario_bp.route('/entrada', methods=['GET', 'POST'])
@role_required('chef')
def entrada():
    """Registrar entrada de inventario"""
    if request.method == 'POST':
        insumo_id = request.form['insumo_id']
        cantidad = float(request.form['cantidad'])
        motivo = request.form['motivo']
        
        if not all([insumo_id, cantidad, motivo]):
            flash('Por favor completa todos los campos', 'error')
            return render_template('inventario/entrada.html', insumos=Insumo.get_all())
        
        if cantidad <= 0:
            flash('La cantidad debe ser mayor a cero', 'error')
            return render_template('inventario/entrada.html', insumos=Insumo.get_all())
        
        try:
            MovimientoInventario.registrar_entrada(
                insumo_id=insumo_id,
                cantidad=cantidad,
                motivo=motivo,
                usuario_id=session['user_id']
            )
            
            flash('Entrada registrada exitosamente', 'success')
            return redirect(url_for('inventario.index'))
            
        except Exception as e:
            flash('Error al registrar la entrada', 'error')
    
    insumos = Insumo.get_all()
    return render_template('inventario/entrada.html', insumos=insumos)

@inventario_bp.route('/salida', methods=['GET', 'POST'])
@role_required('chef')
def salida():
    """Registrar salida de inventario"""
    if request.method == 'POST':
        insumo_id = request.form['insumo_id']
        cantidad = float(request.form['cantidad'])
        motivo = request.form['motivo']
        
        if not all([insumo_id, cantidad, motivo]):
            flash('Por favor completa todos los campos', 'error')
            return render_template('inventario/salida.html', insumos=Insumo.get_all())
        
        if cantidad <= 0:
            flash('La cantidad debe ser mayor a cero', 'error')
            return render_template('inventario/salida.html', insumos=Insumo.get_all())
        
        # Verificar stock disponible
        insumo = Insumo.find_by_id(insumo_id)
        if not insumo or insumo.cantidad_actual < cantidad:
            flash('Stock insuficiente para realizar la salida', 'error')
            return render_template('inventario/salida.html', insumos=Insumo.get_all())
        
        try:
            MovimientoInventario.registrar_salida(
                insumo_id=insumo_id,
                cantidad=cantidad,
                motivo=motivo,
                usuario_id=session['user_id']
            )
            
            flash('Salida registrada exitosamente', 'success')
            return redirect(url_for('inventario.index'))
            
        except Exception as e:
            flash('Error al registrar la salida', 'error')
    
    insumos = Insumo.get_all()
    return render_template('inventario/salida.html', insumos=insumos)

@inventario_bp.route('/api/alertas')
@role_required('chef')
def alertas_stock():
    """API para obtener alertas de stock bajo"""
    insumos_bajo_stock = Insumo.get_low_stock()
    
    alertas = []
    for insumo in insumos_bajo_stock:
        alertas.append({
            'id': insumo.id,
            'nombre': insumo.nombre,
            'cantidad_actual': insumo.cantidad_actual,
            'cantidad_minima': insumo.cantidad_minima,
            'unidad_medida': insumo.unidad_medida
        })
    
    return jsonify({
        'success': True,
        'alertas': alertas,
        'total_alertas': len(alertas)
    })
