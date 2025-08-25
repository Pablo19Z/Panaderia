from flask import Blueprint, render_template, send_file
import io
import base64

main_bp = Blueprint('main', __name__)

@main_bp.route('/placeholder.svg')
def placeholder_svg():
    """Genera SVGs placeholder dinámicos"""
    from flask import request
    
    width = request.args.get('width', 300, type=int)
    height = request.args.get('height', 200, type=int)
    query = request.args.get('query', 'Imagen')
    
    # Crear SVG simple con texto
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2"/>
    <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="16" 
          text-anchor="middle" dominant-baseline="middle" fill="#6c757d">
        {query}
    </text>
    <text x="50%" y="65%" font-family="Arial, sans-serif" font-size="12" 
          text-anchor="middle" dominant-baseline="middle" fill="#adb5bd">
        {width} × {height}
    </text>
</svg>'''
    
    return svg_content, 200, {'Content-Type': 'image/svg+xml'}
