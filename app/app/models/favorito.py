import sqlite3
from . import get_db_connection

class Favorito:
    @staticmethod
    def toggle(user_id, producto_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe
        cursor.execute('''
            SELECT id FROM favoritos 
            WHERE usuario_id = ? AND producto_id = ?
        ''', (user_id, producto_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Eliminar de favoritos
            cursor.execute('DELETE FROM favoritos WHERE id = ?', (existing[0],))
            conn.commit()
            conn.close()
            return False
        else:
            # Agregar a favoritos
            cursor.execute('''
                INSERT INTO favoritos (usuario_id, producto_id)
                VALUES (?, ?)
            ''', (user_id, producto_id))
            conn.commit()
            conn.close()
            return True
    
    @staticmethod
    def find_by_user_and_product(user_id, producto_id):
        """Buscar favorito por usuario y producto"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM favoritos 
            WHERE usuario_id = ? AND producto_id = ?
        ''', (user_id, producto_id))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def create(user_id, producto_id):
        """Crear nuevo favorito"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO favoritos (usuario_id, producto_id)
            VALUES (?, ?)
        ''', (user_id, producto_id))
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def delete(user_id, producto_id):
        """Eliminar favorito"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM favoritos 
            WHERE usuario_id = ? AND producto_id = ?
        ''', (user_id, producto_id))
        
        conn.commit()
        conn.close()
        return True
