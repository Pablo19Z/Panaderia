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
