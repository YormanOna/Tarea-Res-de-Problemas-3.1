import 'package:flutter/material.dart';
import 'dart:async';
import '../controladores/controlador_chat.dart';
import '../modelos/mensaje.dart';

class PantallaChat extends StatefulWidget {
  final String usuario;

  PantallaChat({required this.usuario, Key? key}) : super(key: key);

  @override
  _PantallaChatState createState() => _PantallaChatState();
}

class _PantallaChatState extends State<PantallaChat> {
  final ControladorChat _controladorChat = ControladorChat();
  final TextEditingController _controladorMensaje = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  List<Mensaje> _mensajes = [];
  bool _cargando = true;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _inicializarChat();
    // Configurar actualización automática cada 3 segundos
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      _actualizarMensajes();
    });
  }

  void _inicializarChat() async {
    await _cargarMensajes();
    _controladorChat.conectarSocket(widget.usuario, _recibirMensaje);
  }

  @override
  void dispose() {
    _timer?.cancel();
    _controladorChat.desconectarSocket();
    _controladorMensaje.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _actualizarMensajes() async {
    try {
      final nuevosMensajes = await _controladorChat.obtenerMensajes();
      if (mounted) {
        setState(() {
          _mensajes = nuevosMensajes;
          _mensajes.sort((a, b) => a.hora.compareTo(b.hora));
        });
        _scrollAlFinal();
      }
    } catch (e) {
      print('Error al actualizar mensajes: $e');
    }
  }

  Future<void> _cargarMensajes() async {
    try {
      setState(() => _cargando = true);
      final mensajes = await _controladorChat.obtenerMensajes();
      if (mounted) {
        setState(() {
          _mensajes = mensajes;
          _mensajes.sort((a, b) => a.hora.compareTo(b.hora));
          _cargando = false;
        });
        _scrollAlFinal();
      }
    } catch (e) {
      print('Error al cargar mensajes: $e');
      if (mounted) {
        setState(() => _cargando = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error al cargar mensajes')),
        );
      }
    }
  }

  void _recibirMensaje(Mensaje mensaje) {
    if (mounted) {
      setState(() {
        if (!_mensajes.any((m) =>
            m.remitente == mensaje.remitente &&
            m.texto == mensaje.texto &&
            m.hora == mensaje.hora)) {
          _mensajes.add(mensaje);
          _mensajes.sort((a, b) => a.hora.compareTo(b.hora));
        }
      });
      _scrollAlFinal();
    }
  }

  Future<void> _enviarMensaje() async {
    if (_controladorMensaje.text.isEmpty) return;

    final texto = _controladorMensaje.text;
    _controladorMensaje.clear();

    try {
      final mensaje = Mensaje(
        remitente: widget.usuario,
        receptor: "general",
        texto: texto,
        hora: DateTime.now(),
      );

      // Agregar el mensaje localmente de inmediato
      setState(() {
        _mensajes.add(mensaje);
        _mensajes.sort((a, b) => a.hora.compareTo(b.hora));
      });
      _scrollAlFinal();

      // Enviar el mensaje
      await _controladorChat.enviarMensaje(mensaje);
      
      // Actualizar los mensajes después de enviar
      await _actualizarMensajes();
    } catch (e) {
      print('Error al enviar mensaje: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error al enviar el mensaje')),
        );
      }
    }
  }

  void _scrollAlFinal() {
    if (_scrollController.hasClients) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent + 50,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Fondo sutil y elegante
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: Text('Sala de Chat'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _actualizarMensajes,
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: _cargando
                ? Center(child: CircularProgressIndicator())
                : RefreshIndicator(
                    onRefresh: _actualizarMensajes,
                    child: ListView.builder(
                      controller: _scrollController,
                      physics: AlwaysScrollableScrollPhysics(),
                      itemCount: _mensajes.length,
                      itemBuilder: (context, index) {
                        final msg = _mensajes[index];
                        final esMio = msg.remitente == widget.usuario;
                        return Align(
                          alignment: esMio
                              ? Alignment.centerRight
                              : Alignment.centerLeft,
                          child: Container(
                            constraints: BoxConstraints(
                              maxWidth: MediaQuery.of(context).size.width * 0.4,
                            ),
                            margin: EdgeInsets.symmetric(
                                vertical: 6, horizontal: 12),
                            padding: EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: esMio ? Colors.blueAccent : Colors.white,
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black12,
                                  offset: Offset(0, 1),
                                  blurRadius: 3,
                                )
                              ],
                              borderRadius: BorderRadius.only(
                                topLeft: Radius.circular(12),
                                topRight: Radius.circular(12),
                                bottomLeft:
                                    esMio ? Radius.circular(12) : Radius.circular(0),
                                bottomRight:
                                    esMio ? Radius.circular(0) : Radius.circular(12),
                              ),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      esMio
                                          ? Icons.person
                                          : Icons.person_outline,
                                      size: 16,
                                      color: esMio ? Colors.white : Colors.black,
                                    ),
                                    SizedBox(width: 5),
                                    Text(
                                      msg.remitente,
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: esMio ? Colors.white : Colors.black,
                                      ),
                                    ),
                                  ],
                                ),
                                SizedBox(height: 6),
                                Text(
                                  msg.texto,
                                  style: TextStyle(
                                    color: esMio ? Colors.white : Colors.black87,
                                  ),
                                ),
                                SizedBox(height: 6),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.end,
                                  children: [
                                    Icon(
                                      Icons.access_time,
                                      size: 12,
                                      color: esMio ? Colors.white70 : Colors.grey[600],
                                    ),
                                    SizedBox(width: 3),
                                    Text(
                                      "${msg.hora.day.toString().padLeft(2, '0')}/${msg.hora.month.toString().padLeft(2, '0')}/${msg.hora.year} ${msg.hora.hour.toString().padLeft(2, '0')}:${msg.hora.minute.toString().padLeft(2, '0')}",
                                      style: TextStyle(
                                        fontSize: 10,
                                        color:
                                            esMio ? Colors.white70 : Colors.grey[600],
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
          ),
          // Caja de entrada de mensaje elegante
          Container(
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black26,
                  offset: Offset(0, -1),
                  blurRadius: 4,
                ),
              ],
            ),
            padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 5),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controladorMensaje,
                    decoration: InputDecoration(
                      hintText: 'Escribe un mensaje...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(25),
                        borderSide: BorderSide.none,
                      ),
                      fillColor: Colors.grey[200],
                      filled: true,
                      contentPadding:
                          EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    ),
                    onSubmitted: (_) => _enviarMensaje(),
                  ),
                ),
                SizedBox(width: 8),
                IconButton(
                  icon: Icon(Icons.send, color: Colors.blueAccent),
                  onPressed: _enviarMensaje,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
