from . import get_db_connection

class HistoriaImages:
    """Modelo para gestionar las imágenes de la página de historia"""
    
    @staticmethod
    def create_table():
        """Crea la tabla de imágenes de historia si no existe"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historia_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                image_url TEXT NOT NULL,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_image(key):
        """Obtiene la URL de una imagen por su clave"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT image_url FROM historia_images WHERE setting_key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    @staticmethod
    def set_image(key, url, description=''):
        """Establece o actualiza la URL de una imagen"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO historia_images (setting_key, image_url, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(setting_key) DO UPDATE SET
                image_url = excluded.image_url,
                description = excluded.description,
                updated_at = CURRENT_TIMESTAMP
        ''', (key, url, description))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_images():
        """Obtiene todas las imágenes configuradas"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT setting_key, image_url, description FROM historia_images')
        results = cursor.fetchall()
        conn.close()
        
        images = {}
        for row in results:
            images[row[0]] = {
                'url': row[1],
                'description': row[2]
            }
        return images
    
    @staticmethod
    def initialize_defaults():
        """Inicializa las imágenes por defecto"""
        defaults = {
            'hero_background': ('/placeholder.svg?height=500&width=1200', 'Imagen de fondo del hero de historia'),
            'inicios_image': ('/placeholder.svg?height=400&width=600', 'Imagen de la sección Los Inicios'),
            'timeline_1985': ('/placeholder.svg?height=150&width=200', 'Imagen timeline 1985 - Los Primeros Pasos'),
            'timeline_1995': ('/placeholder.svg?height=150&width=200', 'Imagen timeline 1995 - Primera Expansión'),
            'timeline_2010': ('/placeholder.svg?height=150&width=200', 'Imagen timeline 2010 - Segunda Generación'),
            'timeline_2024': ('/placeholder.svg?height=150&width=200', 'Imagen timeline 2024 - Era Digital'),
            'valores_image': ('/placeholder.svg?height=400&width=600', 'Imagen de la sección Nuestros Valores')
        }
        
        for key, (url, description) in defaults.items():
            if not HistoriaImages.get_image(key):
                HistoriaImages.set_image(key, url, description)
