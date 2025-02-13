from app.config import db

def save_message(message_data):
    """Guarda un mensaje en Firestore."""
    db.collection("mensajes").add(message_data)

def get_messages():
    """Obtiene y retorna todos los mensajes de Firestore."""
    return [doc.to_dict() for doc in db.collection("mensajes").order_by("hora").stream()]
