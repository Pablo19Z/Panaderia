from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify, send_file
from app.models.usuario import Usuario
from app.models.venta import Venta
from app.models.producto import Producto
from app.utils.decorators import admin_required
from datetime import datetime, timedelta
import calendar
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from io import BytesIO
import base64
import os
import random
from app.utils.reportes import generador_reportes

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/vendedor/<int:vendedor_id>/pdf')
@admin_required
def reporte_vendedor_pdf(vendedor_id):
    """Genera reporte PDF de ventas por vendedor"""
    vendedor = Usuario.find_by_id(vendedor_id)
    if not vendedor or vendedor.rol != 'vendedor':
        flash('Vendedor no encontrado', 'error')
        return redirect(url_for('usuarios.personal'))
    
    # Obtener fecha actual y del mes
    fecha_actual = datetime.now()
    primer_dia_mes = fecha_actual.replace(day=1)
    
    # Obtener ventas del vendedor en el mes actual
    ventas_mes = Venta.get_ventas_by_vendedor_mes(vendedor_id, fecha_actual.year, fecha_actual.month)
    
    # Crear PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Título del reporte
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    
    story.append(Paragraph(f"Reporte de Ventas - {vendedor.nombre}", title_style))
    story.append(Paragraph(f"Período: {calendar.month_name[fecha_actual.month]} {fecha_actual.year}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Resumen estadístico
    total_ventas = sum(venta.total for venta in ventas_mes)
    total_pedidos = len(ventas_mes)
    promedio_venta = total_ventas / total_pedidos if total_pedidos > 0 else 0
    
    resumen_data = [
        ['Métrica', 'Valor'],
        ['Total de Pedidos', str(total_pedidos)],
        ['Total Vendido', f'${total_ventas:.2f} COP'],
        ['Promedio por Pedido', f'${promedio_venta:.2f} COP'],
        ['Período', f"{calendar.month_name[fecha_actual.month]} {fecha_actual.year}"]
    ]
    
    resumen_table = Table(resumen_data, colWidths=[2*inch, 2*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(resumen_table)
    story.append(Spacer(1, 30))
    
    # Detalle de ventas
    story.append(Paragraph("Detalle de Ventas", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    if ventas_mes:
        ventas_data = [['Fecha', 'Pedido #', 'Cliente', 'Total', 'Estado']]
        
        for venta in ventas_mes:
            cliente = Usuario.find_by_id(venta.usuario_id)
            cliente_nombre = cliente.nombre if cliente else 'Cliente no encontrado'
            
            ventas_data.append([
                venta.fecha_pedido.strftime('%d/%m/%Y'),
                str(venta.id),
                cliente_nombre,
                f'${venta.total:.2f}',
                venta.estado.title()
            ])
        
        ventas_table = Table(ventas_data, colWidths=[1.2*inch, 0.8*inch, 2*inch, 1*inch, 1*inch])
        ventas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        
        story.append(ventas_table)
    else:
        story.append(Paragraph("No hay ventas registradas en este período.", styles['Normal']))
    
    # Pie de página
    story.append(Spacer(1, 50))
    story.append(Paragraph(f"Reporte generado el {fecha_actual.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Paragraph("Migas de oro Dorè - Sistema de Gestión", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    # Crear respuesta
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=reporte_vendedor_{vendedor.nombre}_{fecha_actual.strftime("%Y_%m")}.pdf'
    
    return response

@reportes_bp.route('/personal/pdf')
@admin_required
def reporte_personal_pdf():
    """Genera reporte PDF general del personal"""
    fecha_actual = datetime.now()
    
    # Obtener personal activo
    vendedores = Usuario.get_by_role('vendedor')
    chefs = Usuario.get_by_role('chef')
    
    # Calcular estadísticas
    for vendedor in vendedores:
        ventas_mes = Venta.get_ventas_by_vendedor_mes(vendedor.id, fecha_actual.year, fecha_actual.month)
        vendedor.ventas_mes = sum(venta.total for venta in ventas_mes)
        vendedor.pedidos_mes = len(ventas_mes)
    
    # Crear PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1
    )
    
    story.append(Paragraph("Reporte General de Personal", title_style))
    story.append(Paragraph(f"Período: {calendar.month_name[fecha_actual.month]} {fecha_actual.year}", styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Resumen vendedores
    story.append(Paragraph("Rendimiento de Vendedores", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    vendedores_data = [['Vendedor', 'Email', 'Pedidos', 'Total Vendido', 'Estado']]
    
    for vendedor in vendedores:
        vendedores_data.append([
            vendedor.nombre,
            vendedor.email,
            str(vendedor.pedidos_mes),
            f'${vendedor.ventas_mes:.2f}',
            'Activo' if vendedor.activo else 'Inactivo'
        ])
    
    vendedores_table = Table(vendedores_data, colWidths=[1.5*inch, 2*inch, 0.8*inch, 1.2*inch, 0.8*inch])
    vendedores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(vendedores_table)
    story.append(Spacer(1, 30))
    
    # Resumen chefs
    story.append(Paragraph("Personal de Cocina", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    chefs_data = [['Chef', 'Email', 'Teléfono', 'Estado']]
    
    for chef in chefs:
        chefs_data.append([
            chef.nombre,
            chef.email,
            chef.telefono or 'No registrado',
            'Activo' if chef.activo else 'Inactivo'
        ])
    
    chefs_table = Table(chefs_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
    chefs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(chefs_table)
    
    # Estadísticas generales
    story.append(Spacer(1, 30))
    story.append(Paragraph("Estadísticas Generales", styles['Heading2']))
    
    total_vendedores_activos = len([v for v in vendedores if v.activo])
    total_chefs_activos = len([c for c in chefs if c.activo])
    total_ventas_mes = sum(v.ventas_mes for v in vendedores)
    total_pedidos_mes = sum(v.pedidos_mes for v in vendedores)
    
    stats_data = [
        ['Métrica', 'Valor'],
        ['Vendedores Activos', str(total_vendedores_activos)],
        ['Chefs Activos', str(total_chefs_activos)],
        ['Total Ventas del Mes', f'${total_ventas_mes:.2f} COP'],
        ['Total Pedidos del Mes', str(total_pedidos_mes)]
    ]
    
    stats_table = Table(stats_data, colWidths=[2.5*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(stats_table)
    
    # Pie de página
    story.append(Spacer(1, 50))
    story.append(Paragraph(f"Reporte generado el {fecha_actual.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Paragraph("Migas de oro Dorè - Sistema de Gestión", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    # Crear respuesta
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=reporte_personal_{fecha_actual.strftime("%Y_%m")}.pdf'
    
    return response

@reportes_bp.route('/ventas/dashboard')
@admin_required
def dashboard_ventas():
    """Dashboard de reportes de ventas con gráficos"""
    fecha_actual = datetime.now()
    
    # Obtener datos para gráficos
    ventas_diarias = Venta.get_ventas_diarias_mes(fecha_actual.year, fecha_actual.month)
    productos_mas_vendidos = Producto.get_mas_vendidos_mes(fecha_actual.year, fecha_actual.month)
    vendedores_top = Usuario.get_vendedores_top_mes(fecha_actual.year, fecha_actual.month)
    
    return render_template('reportes/dashboard.html',
                         ventas_diarias=ventas_diarias,
                         productos_mas_vendidos=productos_mas_vendidos,
                         vendedores_top=vendedores_top,
                         mes_actual=calendar.month_name[fecha_actual.month],
                         año_actual=fecha_actual.year)

@reportes_bp.route('/graficos/ventas')
@admin_required
def graficos_ventas():
    """Genera datos de ventas en formato JSON para el dashboard"""
    try:
        graficos, datos = generador_reportes.generar_todos_los_graficos()
        return jsonify({
            'success': True,
            'graficos': graficos,
            'datos': {
                'total_ventas': float(sum(datos['ventas_diarias'])),
                'promedio_diario': float(sum(datos['ventas_diarias']) / len(datos['ventas_diarias'])),
                'productos_activos': len(datos['productos']),
                'vendedores_activos': len(datos['vendedores'])
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reportes_bp.route('/pdf/completo')
@admin_required
def reporte_completo_pdf():
    """Genera reporte PDF completo con análisis detallado"""
    try:
        datos = generador_reportes.generar_datos_ejemplo()
        
        # Generar PDF con nombre único
        fecha_actual = datetime.now()
        nombre_archivo = f'reporte_completo_{fecha_actual.strftime("%Y_%m_%d_%H%M%S")}.pdf'
        ruta_archivo = os.path.join('app', 'static', 'reportes', nombre_archivo)
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        
        # Generar el PDF
        archivo_generado = generador_reportes.generar_reporte_pdf(datos, ruta_archivo)
        
        # Enviar archivo como descarga
        return send_file(archivo_generado, 
                        as_attachment=True, 
                        download_name=f'reporte_migas_oro_{fecha_actual.strftime("%Y_%m")}.pdf',
                        mimetype='application/pdf')
        
    except Exception as e:
        flash(f'Error generando reporte: {str(e)}', 'error')
        return redirect(url_for('reportes.dashboard_ventas'))

@reportes_bp.route('/dashboard/avanzado')
@admin_required
def dashboard_avanzado():
    """Dashboard avanzado con datos para gráficos"""
    fecha_actual = datetime.now()
    
    try:
        # Generar datos para gráficos
        graficos, datos = generador_reportes.generar_todos_los_graficos()
        
        # Calcular métricas adicionales
        metricas = {
            'total_ventas_mes': sum(datos['ventas_diarias']),
            'promedio_diario': sum(datos['ventas_diarias']) / len(datos['ventas_diarias']),
            'mejor_dia': max(datos['ventas_diarias']),
            'producto_estrella': datos['productos'][0],
            'vendedor_mes': datos['vendedores'][0],
            'crecimiento_clientes': ((datos['nuevos_clientes'][-1] - datos['nuevos_clientes'][0]) / datos['nuevos_clientes'][0]) * 100
        }
        
        return render_template('reportes/dashboard_avanzado.html',
                             graficos=graficos,
                             datos=datos,
                             metricas=metricas,
                             mes_actual=calendar.month_name[fecha_actual.month],
                             año_actual=fecha_actual.year)
        
    except Exception as e:
        flash(f'Error cargando dashboard: {str(e)}', 'error')
        return redirect(url_for('dashboard.admin'))

@reportes_bp.route('/api/datos-tiempo-real')
@admin_required
def datos_tiempo_real():
    """API para obtener datos en tiempo real para gráficos dinámicos"""
    try:
        # Simular datos en tiempo real
        fecha_actual = datetime.now()
        
        # Generar datos actualizados
        productos_opciones = ['Pan Francés', 'Croissant', 'Torta de Chocolate']
        datos_actuales = {
            'ventas_hoy': random.randint(15000, 35000),
            'pedidos_hoy': random.randint(20, 45),
            'clientes_nuevos_hoy': random.randint(2, 8),
            'producto_mas_vendido_hoy': random.choice(productos_opciones),
            'timestamp': fecha_actual.isoformat()
        }
        
        return jsonify({
            'success': True,
            'datos': datos_actuales,
            'ultima_actualizacion': fecha_actual.strftime('%H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
