from firebase_admin import messaging

def send_push_notification(message):
    """
    Enviar una notificación push a todos los dispositivos suscritos al tema 'general'.
    """
    msg = messaging.Message(
        notification=messaging.Notification(
            title="Nuevo mensaje",
            body=message
        ),
        topic="general"  # Se utiliza un tema en lugar de un token
    )
    response = messaging.send(msg)
    return response
