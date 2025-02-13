from firebase_admin import auth

def register_user(email: str, password: str):
    user = auth.create_user(email=email, password=password)
    return {"id": user.uid, "email": user.email}

def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except:
        return None
    
def verify_user_credentials(email: str, password: str) -> bool:
    try:
        # Firebase no permite directamente validar contraseñas desde el servidor
        # Por lo tanto, usa una estrategia alternativa como verificar el inicio de sesión desde el cliente
        user = auth.get_user_by_email(email)
        # Aquí debes implementar una validación personalizada si fuera necesario
        return True  # Suponiendo que las credenciales sean válidas
    except Exception:
        return False