from . import get_db_connection

class Roles:
    ROLES_DISPONIBLES = ['cliente', 'admin', 'vendedor', 'chef']
    
    PERMISOS = {
        'cliente': [
            'ver_productos',
            'agregar_carrito',
            'realizar_pedidos',
            'ver_mis_pedidos',
            'escribir_resenas',
            'usar_chatbot'
        ],
        'vendedor': [
            'ver_productos',
            'gestionar_pedidos',
            'ver_clientes',
            'procesar_ventas',
            'ver_estadisticas_ventas'
        ],
        'chef': [
            'ver_pedidos_cocina',
            'actualizar_estado_pedidos',
            'ver_recetas',
            'gestionar_produccion',
            'gestionar_inventario',
            'ver_estadisticas_produccion',
            'supervisar_cocina',
            'usar_insumos',
            'marcar_pedidos_listos'
        ],
        'admin': [
            'gestionar_usuarios',
            'gestionar_productos',
            'gestionar_categorias',
            'gestionar_inventario',
            'ver_todas_estadisticas',
            'configurar_sistema',
            'gestionar_roles',
            'ver_reportes_completos'
        ]
    }
    
    @staticmethod
    def create_table():
        """Crea tabla de roles (no necesaria, se maneja en usuarios)"""
        pass
    
    @classmethod
    def get_roles_disponibles(cls):
        """Obtiene la lista de roles disponibles"""
        return cls.ROLES_DISPONIBLES
    
    @classmethod
    def get_permisos_rol(cls, rol):
        """Obtiene los permisos de un rol específico"""
        return cls.PERMISOS.get(rol, [])
    
    @classmethod
    def usuario_tiene_permiso(cls, rol, permiso):
        """Verifica si un rol tiene un permiso específico"""
        permisos_rol = cls.get_permisos_rol(rol)
        return permiso in permisos_rol
    
    @classmethod
    def get_descripcion_rol(cls, rol):
        """Obtiene la descripción de un rol"""
        descripciones = {
            'cliente': 'Cliente de la panadería con acceso a compras y pedidos',
            'vendedor': 'Encargado de ventas y atención al cliente',
            'chef': 'Jefe de cocina con supervisión completa de producción y gestión de inventario',
            'admin': 'Administrador con acceso completo al sistema'
        }
        return descripciones.get(rol, 'Rol no definido')
    
    @classmethod
    def puede_acceder_dashboard(cls, rol, dashboard):
        """Verifica si un rol puede acceder a un dashboard específico"""
        accesos = {
            'cliente': ['cliente'],
            'vendedor': ['vendedor'],
            'chef': ['chef'],
            'admin': ['admin', 'vendedor', 'chef']
        }
        return dashboard in accesos.get(rol, [])
