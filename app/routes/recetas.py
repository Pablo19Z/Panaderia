from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.receta import Receta
from app.models.categoria import Categoria
from app.utils.decorators import login_required, admin_or_vendedor_required

recetas_bp = Blueprint('recetas', __name__)

def get_current_user():
    """Obtiene el usuario actual de la sesión"""
    if 'user_id' not in session:
        return None
    from app.models.usuario import Usuario
    return Usuario.find_by_id(session['user_id'])

@recetas_bp.route('/admin/recetas')
@admin_or_vendedor_required
def gestionar_recetas():
    """Página de gestión de recetas para admin y vendedor"""
    recetas_lista = Receta.get_all(include_inactive=True)
    categorias = Categoria.get_all()
    
    return render_template('recetas/gestionar.html', 
                         recetas=recetas_lista,
                         categorias=categorias)

@recetas_bp.route('/admin/recetas/nueva', methods=['GET', 'POST'])
@admin_or_vendedor_required
def crear_receta():
    """Crear nueva receta"""
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.form['nombre'],
                'descripcion': request.form.get('descripcion', ''),
                'ingredientes': request.form.get('ingredientes', ''),
                'instrucciones': request.form.get('instrucciones', ''),
                'tiempo_preparacion': int(request.form.get('tiempo_preparacion', 0)) if request.form.get('tiempo_preparacion') else None,
                'porciones': int(request.form.get('porciones', 1)) if request.form.get('porciones') else None,
                'dificultad': request.form.get('dificultad', 'Media'),
                'categoria_id': int(request.form['categoria_id']) if request.form.get('categoria_id') else None,
                'imagen': request.form.get('imagen', '')
            }
            
            receta_id = Receta.create(data)
            flash(f'Receta "{data["nombre"]}" creada exitosamente.', 'success')
            return redirect(url_for('recetas.gestionar_recetas'))
            
        except ValueError as e:
            flash('Error en los datos de la receta. Verifica los campos numéricos.', 'error')
        except Exception as e:
            flash(f'Error al crear la receta: {str(e)}', 'error')
    
    categorias = Categoria.get_all()
    return render_template('recetas/crear.html', categorias=categorias)

@recetas_bp.route('/admin/recetas/<int:receta_id>/editar', methods=['GET', 'POST'])
@admin_or_vendedor_required
def editar_receta(receta_id):
    """Editar receta existente"""
    receta = Receta.find_by_id(receta_id)
    if not receta:
        flash('Receta no encontrada.', 'error')
        return redirect(url_for('recetas.gestionar_recetas'))
    
    if request.method == 'POST':
        try:
            data = {
                'nombre': request.form['nombre'],
                'descripcion': request.form.get('descripcion', ''),
                'ingredientes': request.form.get('ingredientes', ''),
                'instrucciones': request.form.get('instrucciones', ''),
                'tiempo_preparacion': int(request.form.get('tiempo_preparacion', 0)) if request.form.get('tiempo_preparacion') else None,
                'porciones': int(request.form.get('porciones', 1)) if request.form.get('porciones') else None,
                'dificultad': request.form.get('dificultad', 'Media'),
                'categoria_id': int(request.form['categoria_id']) if request.form.get('categoria_id') else None,
                'imagen': request.form.get('imagen', '')
            }
            
            receta.update(data)
            flash(f'Receta "{data["nombre"]}" actualizada exitosamente.', 'success')
            return redirect(url_for('recetas.gestionar_recetas'))
            
        except ValueError as e:
            flash('Error en los datos de la receta. Verifica los campos numéricos.', 'error')
        except Exception as e:
            flash(f'Error al actualizar la receta: {str(e)}', 'error')
    
    categorias = Categoria.get_all()
    return render_template('recetas/editar.html', receta=receta, categorias=categorias)

@recetas_bp.route('/admin/recetas/<int:receta_id>/eliminar', methods=['POST'])
@admin_or_vendedor_required
def eliminar_receta(receta_id):
    """Eliminar receta (desactivar)"""
    receta = Receta.find_by_id(receta_id)
    if not receta:
        flash('Receta no encontrada.', 'error')
        return redirect(url_for('recetas.gestionar_recetas'))
    
    try:
        receta.update({'activo': False})
        flash(f'Receta "{receta.nombre}" eliminada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar la receta: {str(e)}', 'error')
    
    return redirect(url_for('recetas.gestionar_recetas'))
