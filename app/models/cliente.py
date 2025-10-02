from datetime import datetime
from . import get_db_connection
from .usuario import Usuario

class Cliente(Usuario):
    """Clase Cliente que extiende Usuario con funcionalidades específicas"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @staticmethod
    def create_table():
        """Los clientes usan la misma tabla que usuarios"""
        Usuario.create_table()
    
    @classmethod
    def get_all_clientes(cls):
        """Obtiene todos los usuarios con rol de cliente"""
        return Usuario.get_all(role='cliente')
    
    @classmethod
    def get_estadisticas_clientes(cls):
        """Obtiene estadísticas generales de clientes"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de clientes
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE rol = "cliente" AND activo = 1')
        total_clientes = cursor.fetchone()[0]
        
        # Clientes con pedidos
        cursor.execute('''
            SELECT COUNT(DISTINCT usuario_id) 
            FROM pedidos p 
            JOIN usuarios u ON p.usuario_id = u.id 
            WHERE u.rol = "cliente"
        ''')
        clientes_con_pedidos = cursor.fetchone()[0]
        
        # Cliente con más pedidos
        cursor.execute('''
            SELECT u.nombre, COUNT(p.id) as total_pedidos, SUM(p.total) as total_gastado
            FROM usuarios u
            JOIN pedidos p ON u.id = p.usuario_id
            WHERE u.rol = "cliente" AND u.activo = 1
            GROUP BY u.id
            ORDER BY total_pedidos DESC
            LIMIT 1
        ''')
        top_cliente = cursor.fetchone()
        
        # Nuevos clientes este mes
        cursor.execute('''
            SELECT COUNT(*) 
            FROM usuarios 
            WHERE rol = "cliente" 
            AND strftime('%Y-%m', fecha_registro) = strftime('%Y-%m', 'now')
        ''')
        nuevos_este_mes = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_clientes': total_clientes,
            'clientes_con_pedidos': clientes_con_pedidos,
            'top_cliente': {
                'nombre': top_cliente[0] if top_cliente else 'N/A',
                'pedidos': top_cliente[1] if top_cliente else 0,
                'total_gastado': top_cliente[2] if top_cliente else 0
            },
            'nuevos_este_mes': nuevos_este_mes
        }
    
    @classmethod
    def get_clientes_con_estadisticas(cls):
        """Obtiene clientes con sus estadísticas de compra"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.*, 
                   COUNT(p.id) as total_pedidos,
                   COALESCE(SUM(p.total), 0) as total_gastado,
                   MAX(p.fecha_pedido) as ultimo_pedido,
                   AVG(p.total) as promedio_pedido
            FROM usuarios u
            LEFT JOIN pedidos p ON u.id = p.usuario_id AND p.estado != 'cancelado'
            WHERE u.rol = 'cliente' AND u.activo = 1
            GROUP BY u.id
            ORDER BY total_gastado DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        clientes = []
        for row in rows:
            cliente = cls(*row[:9])  # Los primeros 9 campos son del usuario
            cliente.total_pedidos = row[9]
            cliente.total_gastado = row[10]
            cliente.ultimo_pedido = row[11]
            cliente.promedio_pedido = row[12] if row[12] else 0
            clientes.append(cliente)
        
        return clientes
    
    def get_pedidos(self, estado=None):
        """Obtiene los pedidos del cliente"""
        from .venta import Venta
        return Venta.get_all(estado=estado, usuario_id=self.id)
    
    def get_carrito(self):
        """Obtiene los productos en el carrito del cliente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, p.nombre, p.precio, p.imagen
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.usuario_id = ?
            ORDER BY c.fecha_agregado DESC
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_favoritos(self):
        """Obtiene los productos favoritos del cliente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.*, p.nombre, p.precio, p.imagen, p.descripcion
            FROM favoritos f
            JOIN productos p ON f.producto_id = p.id
            WHERE f.usuario_id = ?
            ORDER BY f.fecha_agregado DESC
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def agregar_al_carrito(self, producto_id, cantidad=1):
        """Agrega un producto al carrito"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si el producto ya está en el carrito
        cursor.execute('SELECT id, cantidad FROM carrito WHERE usuario_id = ? AND producto_id = ?', 
                      (self.id, producto_id))
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar cantidad
            nueva_cantidad = existing[1] + cantidad
            cursor.execute('UPDATE carrito SET cantidad = ? WHERE id = ?', 
                          (nueva_cantidad, existing[0]))
        else:
            # Agregar nuevo item
            cursor.execute('''
                INSERT INTO carrito (usuario_id, producto_id, cantidad)
                VALUES (?, ?, ?)
            ''', (self.id, producto_id, cantidad))
        
        conn.commit()
        conn.close()
    
    def agregar_a_favoritos(self, producto_id):
        """Agrega un producto a favoritos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO favoritos (usuario_id, producto_id)
                VALUES (?, ?)
            ''', (self.id, producto_id))
            conn.commit()
            return True
        except:
            # Ya existe en favoritos
            return False
        finally:
            conn.close()
    
    def remover_de_favoritos(self, producto_id):
        """Remueve un producto de favoritos"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM favoritos WHERE usuario_id = ? AND producto_id = ?', 
                      (self.id, producto_id))
        conn.commit()
        conn.close()
    
    def vaciar_carrito(self):
        """Vacía el carrito del cliente"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM carrito WHERE usuario_id = ?', (self.id,))
        conn.commit()
        conn.close()
    
    def get_total_carrito(self):
        """Calcula el total del carrito"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(c.cantidad * p.precio)
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.usuario_id = ?
        ''', (self.id,))
        result = cursor.fetchone()[0]
        conn.close()
        return result or 0
    
    def contar_items_carrito(self):
        """Cuenta los items en el carrito"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(cantidad) FROM carrito WHERE usuario_id = ?', (self.id,))
        result = cursor.fetchone()[0]
        conn.close()
        return result or 0
    
    def escribir_resena(self, producto_id, calificacion, comentario):
        """Escribe una reseña para un producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya escribió una reseña para este producto
        cursor.execute('SELECT id FROM resenas WHERE usuario_id = ? AND producto_id = ?', 
                      (self.id, producto_id))
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar reseña existente
            cursor.execute('''
                UPDATE resenas SET calificacion = ?, comentario = ?, fecha_resena = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (calificacion, comentario, existing[0]))
        else:
            # Crear nueva reseña
            cursor.execute('''
                INSERT INTO resenas (usuario_id, producto_id, calificacion, comentario)
                VALUES (?, ?, ?, ?)
            ''', (self.id, producto_id, calificacion, comentario))
        
        conn.commit()
        conn.close()
