from fastapi import APIRouter, HTTPException
from firebase_admin import auth
from app.models import User
from app.config import *

router = APIRouter()

@router.post("/register")
async def register(user: User):
    """
    Registrar un nuevo usuario en Firebase Authentication.
    """
    try:
        # Crear el usuario en Firebase Authentication
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        return {"message": f"Usuario {user.email} registrado exitosamente", "uid": user_record.uid}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {e}")

@router.post("/login")
async def login(user: User):
    """
    Iniciar sesión con Firebase Authentication.
    """
    try:
        user_record = auth.get_user_by_email(user.email)
        return {"message": f"Usuario {user.email} logueado correctamente", "uid": user_record.uid}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {e}")
