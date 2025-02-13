from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Conectar a MongoDB (asegúrate de que la URI sea la correcta)
client = MongoClient("mongodb+srv://team:SIANSHYO@cluster0.ccwlf.mongodb.net/contactos_db")
db = client.get_database()  
messages_collection = db.mensajes  # Usamos la colección 'mensajes'

def save_message(message_data):
    """
    Guarda un mensaje en MongoDB.
    """
    message_data['hora'] = datetime.utcnow()  # Asegúrate de agregar la hora si no está
    messages_collection.insert_one(message_data)
    return {"message": "Mensaje enviado"}

def get_messages():
    """
    Obtiene todos los mensajes de MongoDB y los devuelve ordenados por la hora.
    """
    msgs = list(messages_collection.find().sort("hora", 1))  # Ordenar por la hora
    for msg in msgs:
        msg["_id"] = str(msg["_id"])  # Convertir ObjectId en una cadena para evitar errores de serialización
    return msgs
