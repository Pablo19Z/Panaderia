from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
import io
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import random

class GeneradorReportes:
    def __init__(self):
        self.colores_panaderia = {
            'dorado': '#d4af37',
            'marron': '#8B4513',
            'crema': '#F5F5DC',
            'naranja': '#FF9800',
            'verde': '#4CAF50',
            'azul': '#2196F3',
            'morado': '#9C27B0'
        }
        
    def generar_datos_ejemplo(self):
        """Genera datos de ejemplo para los reportes"""
        # Datos de ventas por día (último mes)
        fechas = []
        fecha_inicio = datetime(2024, 11, 17)
        for i in range(30):
            fechas.append(fecha_inicio + timedelta(days=i))
        
        # Generar ventas diarias con random
        ventas_diarias = []
        for _ in range(len(fechas)):
            venta = random.normalvariate(20000, 5000)
            ventas_diarias.append(max(venta, 5000))  # Mínimo 5000
        
        # Datos de productos más vendidos
        productos = ['Pan Francés', 'Croissant', 'Torta de Chocolate', 'Pan Integral', 'Empanadas', 'Galletas']
        ventas_productos = [850, 720, 450, 380, 320, 280]
        
        # Datos de ventas por vendedor
        vendedores = ['María González', 'Carlos Ruiz', 'Ana Martínez', 'Luis Herrera']
        ventas_vendedores = [85000, 72000, 68000, 55000]
        
        # Datos de clientes por mes
        meses = ['Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        nuevos_clientes = [15, 22, 18, 25, 31]
        
        return {
            'fechas': fechas,
            'ventas_diarias': ventas_diarias,
            'productos': productos,
            'ventas_productos': ventas_productos,
            'vendedores': vendedores,
            'ventas_vendedores': ventas_vendedores,
            'meses': meses,
            'nuevos_clientes': nuevos_clientes
        }
    
    def generar_datos_graficos(self):
        """Genera datos para gráficos sin matplotlib"""
        datos = self.generar_datos_ejemplo()
        
        # Convertir datos para uso en templates HTML
        graficos_data = {
            'ventas_diarias': {
                'labels': [fecha.strftime('%d/%m') for fecha in datos['fechas']],
                'data': [float(venta) for venta in datos['ventas_diarias']]
            },
            'productos_vendidos': {
                'labels': datos['productos'],
                'data': datos['ventas_productos']
            },
            'ventas_vendedores': {
                'labels': datos['vendedores'],
                'data': datos['ventas_vendedores']
            },
            'nuevos_clientes': {
                'labels': datos['meses'],
                'data': datos['nuevos_clientes']
            }
        }
        
        return graficos_data, datos
    
    def generar_reporte_pdf(self, datos, nombre_archivo='reporte_panaderia.pdf'):
        """Genera un reporte completo en PDF"""
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para títulos
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.HexColor('#8B4513'),
            alignment=1  # Centrado
        )
        
        # Título principal
        titulo = Paragraph("Reporte de Ventas - Migas de oro Doré", titulo_style)
        story.append(titulo)
        story.append(Spacer(1, 20))
        
        # Fecha del reporte
        fecha_reporte = Paragraph(f"Fecha del reporte: {datetime.now().strftime('%d/%m/%Y')}", 
                                 styles['Normal'])
        story.append(fecha_reporte)
        story.append(Spacer(1, 20))
        
        # Resumen ejecutivo
        promedio_ventas = sum(datos['ventas_diarias']) / len(datos['ventas_diarias'])
        resumen_data = [
            ['Métrica', 'Valor'],
            ['Ventas Totales del Mes', f"${sum(datos['ventas_diarias']):,.0f}"],
            ['Promedio Diario', f"${promedio_ventas:,.0f}"],
            ['Producto Más Vendido', datos['productos'][0]],
            ['Mejor Vendedor', datos['vendedores'][0]],
            ['Nuevos Clientes', f"{sum(datos['nuevos_clientes'])} clientes"]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d4af37')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Resumen Ejecutivo", styles['Heading2']))
        story.append(resumen_table)
        story.append(Spacer(1, 30))
        
        # Tabla de productos más vendidos
        productos_data = [['Producto', 'Unidades Vendidas', 'Porcentaje']]
        total_productos = sum(datos['ventas_productos'])
        
        for producto, ventas in zip(datos['productos'], datos['ventas_productos']):
            porcentaje = (ventas / total_productos) * 100
            productos_data.append([producto, f"{ventas}", f"{porcentaje:.1f}%"])
        
        productos_table = Table(productos_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        productos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Productos Más Vendidos", styles['Heading2']))
        story.append(productos_table)
        story.append(Spacer(1, 30))
        
        # Tabla de rendimiento por vendedor
        vendedores_data = [['Vendedor', 'Ventas Totales', 'Porcentaje']]
        total_ventas_vendedores = sum(datos['ventas_vendedores'])
        
        for vendedor, ventas in zip(datos['vendedores'], datos['ventas_vendedores']):
            porcentaje = (ventas / total_ventas_vendedores) * 100
            vendedores_data.append([vendedor, f"${ventas:,}", f"{porcentaje:.1f}%"])
        
        vendedores_table = Table(vendedores_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        vendedores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Rendimiento por Vendedor", styles['Heading2']))
        story.append(vendedores_table)
        
        # Construir el PDF
        doc.build(story)
        return nombre_archivo
    
    def generar_todos_los_graficos(self):
        """Genera todos los datos para gráficos sin matplotlib"""
        return self.generar_datos_graficos()

# Instancia global del generador
generador_reportes = GeneradorReportes()
