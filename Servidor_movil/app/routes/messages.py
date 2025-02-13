from fastapi import APIRouter, HTTPException
from app.services.chat_service import save_message, get_messages
from app.models import Message  # Modelo Pydantic para mensajes

router = APIRouter()

@router.get("/messages")
async def messages():
    """
    Obtener todos los mensajes almacenados.
    """
    try:
        msgs = get_messages()  # Obtener mensajes desde MongoDB
        return msgs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener mensajes: {e}")

@router.post("/send")
async def send(msg: Message):
    """
    Guardar un nuevo mensaje.
    """
    try:
        return save_message(msg.dict())  # Guardar mensaje en MongoDB
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar mensaje: {e}")
