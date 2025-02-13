import 'package:flutter/material.dart';
import 'package:mensajes/vistas/pantalla_login.dart';

void main() {
  runApp(MiAplicacion());
}


class MiAplicacion extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Aplicación de Chat',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PantallaLogin(),
    );
  }
}
