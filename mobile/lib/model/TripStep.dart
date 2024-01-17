import 'dart:core';

class TripStep {
  final List<int?> duration_between_stations;
  final List<String> path;
  final String departure;
  final String arrival;

  TripStep({
    required this.duration_between_stations,
    required this.path,
    required this.departure,
    required this.arrival
  });

  factory TripStep.fromJson(Map<String, dynamic> json) {
    return TripStep(
        duration_between_stations: List<int>.from(json['duration_between_stations']),
        path: List<String>.from(json['path']),
        departure: json['departure'],
        arrival: json['arrival']
    );
  }
}