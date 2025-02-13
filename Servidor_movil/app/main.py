# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, messages
import socketio

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

# Eventos Socket.IO
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_success', {'message': 'Successfully connected'})

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def sendMessage(sid, data):
    print(f"Message received: {data}")
    await sio.emit('receiveMessage', data)

@app.get("/")
async def root():
    return {"message": "Chat en tiempo real con FastAPI y Firebase"}

# Es importante que esto sea la última línea
app = socket_app