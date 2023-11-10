class ItineraryResponse {
  final String sentenceID;
  final String departure;
  final String destination;
  final List<String> steps;

  ItineraryResponse({
    required this.sentenceID,
    required this.departure,
    required this.destination,
    required this.steps,
  });

  factory ItineraryResponse.fromJson(Map<String, dynamic> json) {
    return ItineraryResponse(
      sentenceID: json['sentenceID'],
      departure: json['departure'],
      destination: json['destination'],
      steps: List<String>.from(json['steps']),
    );
  }
}
