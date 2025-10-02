"""
Utilidades para formatear precios y otros datos
"""

def formatear_precio(precio):
    """
    Formatea un precio en pesos colombianos
    Ejemplo: 32000 -> "$32.000"
    """
    if precio is None:
        return "$0"
    
    # Convertir a entero si es necesario
    if isinstance(precio, float):
        precio = int(precio)
    
    return f"${precio:,.0f}".replace(",", ".")

def formatear_precio_simple(precio):
    """
    Formatea un precio sin símbolo de peso
    Ejemplo: 32000 -> "32.000"
    """
    if precio is None:
        return "0"
    
    # Convertir a entero si es necesario
    if isinstance(precio, float):
        precio = int(precio)
    
    return f"{precio:,.0f}".replace(",", ".")

def formatear_precio_cop(precio):
    """
    Formatea un precio en pesos colombianos con sufijo COP
    Ejemplo: 32000 -> "$32.000 COP"
    """
    if precio is None:
        return "$0 COP"
    
    # Convertir a entero si es necesario
    if isinstance(precio, float):
        precio = int(precio)
    
    # Formatear con separadores de miles y sufijo COP
    return f"${precio:,.0f} COP".replace(",", ".")
