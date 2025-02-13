# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, messages
import socketio
from app.services.chat_service import save_message

# Crear el servidor Socket.IO
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['*'],
    logger=True,
    engineio_logger=True
)

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear la aplicación ASGI
socket_app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=app,
    socketio_path='socket.io'
)

# Incluir rutas
app.include_router(auth.router, prefix="/auth")
app.include_router(messages.router, prefix="/chat")
connected_users = {}
# Eventos Socket.IO
@sio.event
async def connect(sid, environ):
    """
    Cuando un cliente se conecta, automáticamente se une a la sala "general".
    """
    print(f"Nuevo cliente conectado: {sid}")
    sio.enter_room(sid, "general")  # Asignar a la sala 'general'
    connected_users[sid] = "general"  # Registrar al usuario en la sala 'general'
    print(f"Usuario {sid} se unió a la sala 'general'.")

@sio.event
async def disconnect(sid):
    """
    Limpiar cuando un cliente se desconecta.
    """
    room = connected_users.pop(sid, None)  # Eliminar al usuario del diccionario y de la sala
    if room:
        sio.leave_room(sid, room)
        print(f"Usuario {sid} dejó la sala '{room}' y se desconectó.")
    else:
        print(f"Usuario {sid} se desconectó.")

@sio.event
async def sendMessage(sid, data):
    """
    Al enviar un mensaje, lo guarda en MongoDB y lo retransmite a todos los clientes en la sala actual.
    """
    try:
        room = connected_users.get(sid, "general")  # Obtener la sala del usuario (por defecto 'general')
        save_message(data)  # Guardar el mensaje en MongoDB
        print(f"Mensaje recibido de {data['remitente']} en la sala '{room}': {data['texto']}")
        await sio.emit("receiveMessage", data, room=room)  # Retransmitir el mensaje a la sala
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

@app.get("/")
async def root():
    return {"message": "Chat en tiempo real con FastAPI y Firebase"}

# Es importante que esto sea la última línea
app = socket_app