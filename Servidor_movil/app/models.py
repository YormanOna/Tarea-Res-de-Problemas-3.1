from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    email: str
    password: str

class Message(BaseModel):
    remitente: str
    receptor: str
    texto: str
    hora: Optional[datetime] = datetime.utcnow().isoformat()
