import 'dart:core';

import 'package:mobile/model/TripStep.dart';

class ItineraryResponse {
  final String state;
  final List<TripStep>? steps;

  ItineraryResponse({
    required this.state,
    this.steps
  });

  factory ItineraryResponse.fromJson(Map<String, dynamic> json) {
    return ItineraryResponse(
      state: json['state'],
      steps: json['steps'] != null ? (json['steps'] as List).map((i) => TripStep.fromJson(i)).toList() : null,
    );
  }
}
