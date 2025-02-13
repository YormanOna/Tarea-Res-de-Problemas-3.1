# tests/test_auth.py
import random
import string
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def random_email():
    """Genera un correo aleatorio para evitar colisiones en registros repetidos."""
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=5))}@example.com"

def test_register_new_user():
    """
    Resumen: Registro de usuario nuevo.
    Pasos: Se envía una solicitud POST a /auth/register con un email y password nuevos.
    Entrada: JSON con email y password.
    Condiciones: No existe aún el usuario.
    Resultado esperado: Código 200 y respuesta que incluya el uid y mensaje de éxito.
    """
    email = random_email()
    password = "testpassword"
    response = client.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "uid" in data
    assert "registrado" in data.get("message", "")

def test_successful_login():
    """
    Resumen: Inicio de sesión exitoso.
    Pasos: Primero se registra el usuario y luego se envía solicitud POST a /auth/login.
    Entrada: JSON con email y password válidos.
    Condiciones: Usuario previamente registrado.
    Resultado esperado: Código 200 y respuesta que incluya uid y mensaje de éxito.
    """
    email = random_email()
    password = "testpassword"
    # Registrar el usuario primero
    register_response = client.post("/auth/register", json={"email": email, "password": password})
    assert register_response.status_code == 200
    # Intentar iniciar sesión
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200, login_response.text
    data = login_response.json()
    assert "uid" in data
    assert "logueado" in data.get("message", "")

def test_failed_login():
    """
    Resumen: Inicio de sesión fallido (credenciales incorrectas).
    Pasos: Se envía una solicitud POST a /auth/login con un email no registrado.
    Entrada: JSON con email inexistente y cualquier password.
    Condiciones: Usuario no existe.
    Resultado esperado: Código 404 y mensaje indicando que el usuario no fue encontrado.
    """
    response = client.post("/auth/login", json={"email": "nonexistent@example.com", "password": "whatever"})
    assert response.status_code == 404, response.text
    data = response.json()
    assert "Usuario no encontrado" in data.get("detail", "")
