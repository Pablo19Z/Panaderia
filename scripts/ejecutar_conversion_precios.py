#!/usr/bin/env python3
"""
Script ejecutor para convertir precios a pesos colombianos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar y ejecutar el script de conversión
from scripts.actualizar_precios_pesos_colombianos import actualizar_precios_pesos

if __name__ == '__main__':
    print("🚀 Ejecutando conversión de precios a pesos colombianos...")
    actualizar_precios_pesos()
    print("✅ Conversión completada!")
