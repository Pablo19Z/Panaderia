from . import get_db_connection

class SystemSettings:
    """Modelo para configuraciones del sistema"""
    
    @staticmethod
    def create_table():
        """Crea la tabla de configuraciones del sistema"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar configuración por defecto para hero_background_url si no existe
        cursor.execute('''
            INSERT OR IGNORE INTO system_settings (key, value, description)
            VALUES (?, ?, ?)
        ''', ('hero_background_url', '/placeholder.svg?height=600&width=1200', 'URL de la imagen de fondo del hero en la página de inicio'))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_setting(key):
        """Obtiene el valor de una configuración"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM system_settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        return result[0] if result else None
    
    @staticmethod
    def set_setting(key, value, description=None):
        """Establece o actualiza una configuración"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if description:
            cursor.execute('''
                INSERT INTO system_settings (key, value, description, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    description = excluded.description,
                    updated_at = CURRENT_TIMESTAMP
            ''', (key, value, description))
        else:
            cursor.execute('''
                INSERT INTO system_settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            ''', (key, value))
        
        conn.commit()
        conn.close()
        
        return True
    
    @staticmethod
    def get_all_settings():
        """Obtiene todas las configuraciones"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value, description FROM system_settings')
        results = cursor.fetchall()
        
        conn.close()
        
        return {row[0]: {'value': row[1], 'description': row[2]} for row in results}
