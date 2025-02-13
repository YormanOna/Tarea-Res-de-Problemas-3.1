class Mensaje {
  final String remitente;
  final String receptor;
  final String texto;
  final DateTime hora;

  Mensaje({
    required this.remitente,
    required this.receptor,
    required this.texto,
    required this.hora,
  });

  factory Mensaje.desdeJson(Map<String, dynamic> json) {
    DateTime parsedHora;

    if (json['hora'] is String) {
      // Try parsing an ISO8601 string.
      try {
        parsedHora = DateTime.parse(json['hora']);
      } catch (e) {
        // Fallback if parsing fails.
        parsedHora = DateTime.now();
      }
    } else if (json['hora'] is Map) {
      // Firestore sometimes returns timestamps as a map with _seconds and _nanoseconds.
      try {
        final seconds = json['hora']['_seconds'];
        final nanoseconds = json['hora']['_nanoseconds'] ?? 0;
        parsedHora = DateTime.fromMillisecondsSinceEpoch(
            seconds * 1000 + (nanoseconds / 1000000).round());
      } catch (e) {
        parsedHora = DateTime.now();
      }
    } else {
      // If the field is missing or in an unexpected format.
      parsedHora = DateTime.now();
    }

    return Mensaje(
      remitente: json['remitente'] ?? '',
      receptor: json['receptor'] ?? '',
      texto: json['texto'] ?? '',
      hora: parsedHora,
    );
  }

  Map<String, dynamic> aJson() {
    return {
      'remitente': remitente,
      'receptor': receptor,
      'texto': texto,
      // Always send the time as an ISO8601 string.
      'hora': hora.toIso8601String(),
    };
  }
}
