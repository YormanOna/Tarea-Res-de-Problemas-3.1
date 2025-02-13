from app.database import save_message, get_messages

def send_message(data):
    save_message(data)
    return {"message": "Mensaje enviado"}

def fetch_messages():
    return get_messages()
