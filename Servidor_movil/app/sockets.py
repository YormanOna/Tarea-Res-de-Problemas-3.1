import socketio
from app.services.chat_service import send_message

# Create an Async Socket.IO server in ASGI mode (allowing CORS)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
# Create the ASGI app with a custom socket.io path.
# With the following mount in main.py, clients will use the URL: 
# http://<server>:<port>/ws/socket.io
socket_app = socketio.ASGIApp(sio, socketio_path="socket.io")

# Dictionary to track connected users and their rooms
connected_users = {}

@sio.event
async def connect(sid, environ):
    """
    When a client connects, automatically join the "general" room.
    (No explicit websocket.accept() is needed because the ASGIApp handles it.)
    """
    print(f"[Socket.IO] New connection: {sid}")
    sio.enter_room(sid, "general")
    connected_users[sid] = "general"
    print(f"[Socket.IO] User {sid} connected and joined room 'general'.")

@sio.event
async def joinRoom(sid, room):
    """
    Allow the user to change rooms.
    """
    old_room = connected_users.get(sid, "general")
    sio.leave_room(sid, old_room)
    sio.enter_room(sid, room)
    connected_users[sid] = room
    print(f"[Socket.IO] User {sid} switched from room '{old_room}' to '{room}'.")

@sio.event
async def sendMessage(sid, data):
    """
    When a message is sent, save it (e.g., to Firestore) and broadcast
    it to all clients in the current room.
    """
    room = connected_users.get(sid, "general")
    # Save the message in your database
    send_message(data)
    print(f"[Socket.IO] Message from {data['remitente']} in room '{room}': {data['texto']}")
    await sio.emit("receiveMessage", data, room=room)

@sio.event
async def disconnect(sid):
    """
    Clean up when a client disconnects.
    """
    room = connected_users.pop(sid, None)
    if room:
        sio.leave_room(sid, room)
        print(f"[Socket.IO] User {sid} left room '{room}' and disconnected.")
    else:
        print(f"[Socket.IO] User {sid} disconnected.")
