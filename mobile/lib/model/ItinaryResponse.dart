class ItinaryResponse {
  final String sentenceID;
  final String departure;
  final String destination;
  final List<String> steps;

  ItinaryResponse({
    required this.sentenceID,
    required this.departure,
    required this.destination,
    required this.steps,
  });

  factory ItinaryResponse.fromJson(Map<String, dynamic> json) {
    return ItinaryResponse(
      sentenceID: json['sentenceID'],
      departure: json['departure'],
      destination: json['destination'],
      steps: List<String>.from(json['steps']),
    );
  }
}
