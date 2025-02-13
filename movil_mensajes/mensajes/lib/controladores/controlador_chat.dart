import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:socket_io_client/socket_io_client.dart' as IO;
import '../modelos/mensaje.dart';

class ControladorChat {
  final String apiUrl = 'https://5fc9-177-53-215-61.ngrok-free.app/chat/messages';
  final String sendUrl = 'https://5fc9-177-53-215-61.ngrok-free.app/chat/send';
  final String socketUrl = 'https://5fc9-177-53-215-61.ngrok-free.app';

  IO.Socket? socket;
  Function? _onMessageCallback;

  void conectarSocket(String usuario, Function alRecibirMensaje) {
    _onMessageCallback = alRecibirMensaje;
    
    socket = IO.io(
      socketUrl,
      IO.OptionBuilder()
          .setTransports(['websocket', 'polling'])
          .setPath('/socket.io')  // Cambiado de '/ws/socket.io' a '/socket.io'
          .enableAutoConnect()
          .enableReconnection()
          .setReconnectionAttempts(double.infinity)
          .setReconnectionDelay(1000)
          .build(),
    );

    socket!.onConnect((_) {
      print('🔗 Conectado al WebSocket');
    });

    socket!.onConnectError((data) {
      print('⚠️ Error de conexión: $data');
      // Intenta reconectar después de un error
      Future.delayed(Duration(seconds: 2), () {
        if (socket?.connected == false) {
          socket?.connect();
        }
      });
    });

    socket!.onDisconnect((_) {
      print('❌ Desconectado del WebSocket');
      // Intenta reconectar al desconectarse
      Future.delayed(Duration(seconds: 2), () {
        if (socket?.connected == false) {
          socket?.connect();
        }
      });
    });

    socket!.on('receiveMessage', (data) {
      print("📩 Mensaje recibido: $data");
      if (_onMessageCallback != null) {
        final mensaje = Mensaje.desdeJson(data);
        _onMessageCallback!(mensaje);
      }
    });

    socket!.connect();
  }

  void desconectarSocket() {
    _onMessageCallback = null;
    socket?.disconnect();
    socket?.dispose();
    socket = null;
  }

  Future<List<Mensaje>> obtenerMensajes() async {
    try {
      final respuesta = await http.get(Uri.parse(apiUrl));
      if (respuesta.statusCode == 200) {
        final List decodificado = json.decode(respuesta.body);
        return decodificado.map((data) => Mensaje.desdeJson(data)).toList();
      } else {
        throw Exception('Error al obtener los mensajes: ${respuesta.statusCode}');
      }
    } catch (e) {
      print('Error en obtenerMensajes: $e');
      rethrow;
    }
  }

  Future<void> enviarMensaje(Mensaje mensaje) async {
    try {
      // Primero, emitir por el socket
      if (socket?.connected ?? false) {
        socket?.emit('sendMessage', mensaje.aJson());
        // Llamamos al callback inmediatamente para actualización instantánea
        if (_onMessageCallback != null) {
          _onMessageCallback!(mensaje);
        }
      }

      // Luego, enviar al endpoint HTTP
      final respuesta = await http.post(
        Uri.parse(sendUrl),
        headers: {"Content-Type": "application/json"},
        body: json.encode(mensaje.aJson()),
      );

      if (respuesta.statusCode != 200) {
        throw Exception('Error al enviar el mensaje: ${respuesta.statusCode}');
      }
    } catch (e) {
      print("Error enviando mensaje: $e");
      rethrow;
    }
  }
}