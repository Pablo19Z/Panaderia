# 🔧 Cómo Arreglar el Error de Base de Datos

## Problema
El error "table pedidos has no column named comprobante_pago" ocurre porque la base de datos actual tiene un esquema antiguo sin las columnas necesarias.

## Solución Simple (3 Pasos)

### Paso 1: Detener la Aplicación
Si la aplicación está corriendo, presiona `Ctrl+C` en la terminal para detenerla.

### Paso 2: Resetear la Base de Datos
Ejecuta el script de reseteo:

\`\`\`bash
python scripts/resetear_base_datos.py
\`\`\`

Este script eliminará la base de datos antigua de forma segura.

### Paso 3: Reiniciar la Aplicación
Ejecuta la aplicación normalmente:

\`\`\`bash
python run.py
\`\`\`

La aplicación creará automáticamente una nueva base de datos con el esquema correcto que incluye todas las columnas necesarias:
- `direccion_entrega`
- `telefono_contacto`
- `notas`
- `metodo_pago`
- `fecha_entrega`
- `hora_entrega`
- `comprobante_pago`

## ✅ Resultado
Después de estos pasos:
- Las compras se procesarán correctamente
- Podrás cambiar precios de productos sin problemas
- Los PDFs se generarán sin errores
- El historial de ventas mantendrá los precios originales

## 🔐 Credenciales de Prueba
Después del reseteo, usa estas credenciales:
- **Admin**: admin@migasdeoro.com / admin123
- **Vendedor**: vendedor@migasdeoro.com / vendedor123
- **Cliente**: cliente@test.com / 123456

## ⚠️ Nota Importante
Este proceso eliminará todos los datos actuales (usuarios, productos, pedidos). Si tienes datos importantes, haz un respaldo del archivo `instance/panaderia.db` antes de ejecutar el script de reseteo.
