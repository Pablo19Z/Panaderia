import os

class InstanceConfig:
    """Configuración específica de la instancia"""
    
    # Configuración de la base de datos
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'panaderia.db')
    
    # Configuración de la panadería
    PANADERIA_INFO = {
        'nombre': 'Migas de oro Dorè',
        'direccion': 'Av. Principal 123, Centro',
        'telefono': '+1 234 567 8900',
        'email': 'info@migasdeoro.com',
        'horarios': {
            'lunes_viernes': '6:00 AM - 8:00 PM',
            'sabado': '6:00 AM - 9:00 PM',
            'domingo': '7:00 AM - 6:00 PM'
        },
        'redes_sociales': {
            'facebook': 'https://facebook.com/migasdeoro',
            'instagram': 'https://instagram.com/migasdeoro',
            'whatsapp': '+1234567890'
        }
    }
    
    # Configuración del chatbot
    CHATBOT_RESPONSES = {
        'horarios': 'Nuestros horarios son: Lunes a Viernes 6:00 AM - 8:00 PM, Sábados 6:00 AM - 9:00 PM, Domingos 7:00 AM - 6:00 PM',
        'ubicacion': 'Nos encontramos en Av. Principal 123, Centro. ¡Te esperamos!',
        'delivery': 'Sí, hacemos delivery. El costo es de $3.00 y el tiempo estimado es de 30-45 minutos.',
        'especialidades': 'Nuestras especialidades son: Pan artesanal, Croissants, Pasteles personalizados, Empanadas y Café de especialidad.',
        'contacto': 'Puedes contactarnos al +1 234 567 8900 o escribirnos a info@migasdeoro.com'
    }
