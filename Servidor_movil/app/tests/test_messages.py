# tests/test_messages.py
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_valid_message():
    """
    Resumen: Envío y guardado de mensajes (formato válido).
    Pasos: Se envía una solicitud POST a /chat/send con datos completos.
    Entrada: JSON con remitente, receptor, texto y hora.
    Condiciones: Formato de mensaje válido.
    Resultado esperado: Código 200 y mensaje de confirmación.
    """
    message_data = {
        "remitente": "user1@example.com",
        "receptor": "user2@example.com",
        "texto": "Hola, este es un mensaje de prueba",
        "hora": datetime.utcnow().isoformat()
    }
    response = client.post("/chat/send", json=message_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "Mensaje enviado" in data.get("message", "")

def test_retrieve_messages():
    """
    Resumen: Recuperación de mensajes.
    Pasos: Se envía primero un mensaje y luego se realiza una solicitud GET a /chat/messages.
    Entrada: Ninguna (solo GET).
    Condiciones: Existencia de mensajes.
    Resultado esperado: Código 200 y una lista de mensajes.
    """
    # Asegurarse de que al menos exista un mensaje
    message_data = {
        "remitente": "user1@example.com",
        "receptor": "user2@example.com",
        "texto": "Mensaje para recuperar",
        "hora": datetime.utcnow().isoformat()
    }
    send_response = client.post("/chat/send", json=message_data)
    assert send_response.status_code == 200

    response = client.get("/chat/messages")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    # Se espera que haya al menos un mensaje
    assert len(data) > 0

def test_missing_required_fields():
    """
    Resumen: Validación de campos requeridos.
    Pasos: Se envía una solicitud POST a /chat/send omitiendo el campo "remitente".
    Entrada: JSON incompleto.
    Condiciones: Falta un campo obligatorio.
    Resultado esperado: Código 422 (Unprocessable Entity) por error de validación.
    """
    message_data = {
        # "remitente": "user1@example.com",  # Campo omitido intencionalmente
        "receptor": "user2@example.com",
        "texto": "Mensaje con datos incompletos",
        "hora": datetime.utcnow().isoformat()
    }
    response = client.post("/chat/send", json=message_data)
    assert response.status_code == 422, response.text
