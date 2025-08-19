# 🥖 Panadería Migas de oro Dorè

Sistema completo de gestión para panadería con múltiples roles de usuario y funcionalidades avanzadas.

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**
   \`\`\`bash
   # Si tienes git instalado
   git clone <url-del-repositorio>
   cd panaderia-migas-oro
   \`\`\`

2. **Instalar dependencias**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
   
   O instalar Flask directamente:
   \`\`\`bash
   pip install flask
   \`\`\`

3. **Ejecutar la aplicación**
   \`\`\`bash
   python run.py
   \`\`\`

### Acceso a la Aplicación

Una vez ejecutado el comando anterior, la aplicación estará disponible en:
- **URL**: http://localhost:5000
- **Usuario Admin por defecto**: admin@migasdeoro.com
- **Contraseña Admin**: admin123

## 🎯 Funcionalidades

### Para Visitantes (Sin registro)
- ✅ Ver productos y categorías
- ✅ Añadir productos a favoritos (temporal)
- ✅ Añadir productos al carrito
- ✅ Vaciar carrito

### Para Usuarios Registrados
- ✅ Todas las funcionalidades de visitantes
- ✅ Realizar compras y pagos
- ✅ Acceder al chatbot de ayuda
- ✅ Escribir reseñas de productos
- ✅ Historial de pedidos

### Dashboards por Rol

#### 👥 Clientes
- Ver historial de pedidos
- Gestionar perfil
- Favoritos guardados

#### 👨‍💼 Administradores
- Gestión completa de usuarios
- Gestión de productos y categorías
- Reportes de ventas
- Gestión de inventario

#### 🛒 Vendedores
- Gestión de pedidos
- Atención al cliente
- Reportes de ventas

#### 👨‍🍳 Cocineros
- Ver pedidos pendientes
- Actualizar estado de preparación
- Gestión de recetas

#### 👨‍🍳 Chef/Jefe de Cocina
- Supervisión general
- Gestión de insumos
- Planificación de producción

## 🗄️ Base de Datos

La aplicación utiliza SQLite y se crea automáticamente al ejecutar por primera vez. Incluye:

- **usuarios**: Gestión de usuarios con roles
- **productos**: Catálogo de productos
- **categorias**: Organización de productos
- **carrito**: Carrito de compras temporal
- **favoritos**: Productos favoritos por usuario
- **pedidos**: Historial de pedidos
- **insumos**: Inventario de materias primas
- **resenas**: Reseñas de productos
- **mensajes_chat**: Historial del chatbot

## 🎨 Diseño

- Tema oscuro elegante adaptado para panadería
- Tipografía cursiva para el título "Migas de oro Dorè"
- Diseño responsive para móviles y desktop
- Interfaz intuitiva y moderna

## 🔧 Estructura del Proyecto

\`\`\`
panaderia-migas-oro/
├── run.py              # Archivo principal de ejecución
├── app.py              # Aplicación Flask principal
├── database.py         # Configuración y gestión de SQLite
├── requirements.txt    # Dependencias de Python
├── README.md          # Este archivo
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── templates/         # Plantillas HTML
└── panaderia.db      # Base de datos SQLite (se crea automáticamente)
\`\`\`

## 🆘 Solución de Problemas

### Error: "Flask no está instalado"
\`\`\`bash
pip install flask
\`\`\`

### Error: "Puerto 5000 en uso"
Cambiar el puerto en `run.py` línea final:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar 5000 por 5001
