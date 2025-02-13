from fastapi import APIRouter, HTTPException
from app.services.chat_service import fetch_messages, send_message
from app.models import Message  # Your Pydantic model for Message
from datetime import datetime

router = APIRouter()

@router.get("/messages")
async def messages():
    """
    Retrieve stored messages and sort them by their timestamp.
    (Assumes that the 'hora' field is stored in ISO8601 format.)
    """
    try:
        msgs = fetch_messages()
        try:
            # Sort messages by their 'hora' field (convert the ISO string to datetime)
            msgs.sort(key=lambda m: datetime.fromisoformat(m['hora']))
        except Exception as sort_error:
            print("[Messages Route] Error sorting messages:", sort_error)
        return msgs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener mensajes: {e}")

@router.post("/send")
async def send(msg: Message):
    """
    Save a new message.
    """
    try:
        return send_message(msg.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar mensaje: {e}")
