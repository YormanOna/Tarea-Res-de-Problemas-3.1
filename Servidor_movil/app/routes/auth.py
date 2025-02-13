from fastapi import APIRouter, HTTPException
from app.services.auth_service import register_user, verify_user_credentials
from app.models import User

router = APIRouter()

@router.post("/register")
async def register(user: User):
    """
    Registrar un usuario con correo y contraseña.
    """
    try:
        # Crear el usuario
        firebase_user = register_user(user.email, user.password)
        return {
            "id": firebase_user['id'],
            "email": firebase_user['email'],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")

@router.post("/login")
async def login(user: User):
    """
    Verificar las credenciales del usuario.
    """
    try:
        # Verificar correo y contraseña
        is_valid_user = verify_user_credentials(user.email, user.password)
        if not is_valid_user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        return {"message": "Inicio de sesión exitoso", "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")
