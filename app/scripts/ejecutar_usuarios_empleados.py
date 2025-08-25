#!/usr/bin/env python3
"""
Script para ejecutar la creación de usuarios empleados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.crear_usuarios_empleados import crear_usuarios_empleados

if __name__ == '__main__':
    print("🚀 Ejecutando creación de usuarios empleados...")
    crear_usuarios_empleados()
    print("✅ Proceso completado!")
