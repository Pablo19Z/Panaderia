import sqlite3
from . import get_db_connection

class Carrito:
    @staticmethod
    def agregar_item(user_id, producto_id, cantidad):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe el item
        cursor.execute('''
            SELECT id, cantidad FROM carrito 
            WHERE usuario_id = ? AND producto_id = ?
        ''', (user_id, producto_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar cantidad
            nueva_cantidad = existing[1] + cantidad
            cursor.execute('''
                UPDATE carrito SET cantidad = ? 
                WHERE id = ?
            ''', (nueva_cantidad, existing[0]))
        else:
            # Crear nuevo item
            cursor.execute('''
                INSERT INTO carrito (usuario_id, producto_id, cantidad)
                VALUES (?, ?, ?)
            ''', (user_id, producto_id, cantidad))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_count(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(cantidad) FROM carrito WHERE usuario_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] else 0
