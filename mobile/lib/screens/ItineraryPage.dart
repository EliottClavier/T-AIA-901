import 'package:flutter/material.dart';
import '../model/ItineraryResponse.dart';

class ItineraryPage extends StatelessWidget {
  final ItineraryResponse itineraryResponse;

  ItineraryPage({required this.itineraryResponse});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Itinéraire'),
        actions: [
          IconButton(
            icon: Icon(Icons.home),
            onPressed: () {
              Navigator.of(context).popUntil((route) => route.isFirst);
            },
          )],
      ),
      body: ListView.builder(
        itemCount: itineraryResponse.steps.length + 2,
        itemBuilder: (context, index) {
          if (index == 0) {
            return ListTile(title: Text('Départ: ${itineraryResponse.departure}'));
          } else if (index == itineraryResponse.steps.length + 1) {
            return ListTile(title: Text('Destination: ${itineraryResponse.destination}'));
          } else {
            return ListTile(title: Text('Étape ${index}: ${itineraryResponse.steps[index - 1]}'));
          }
        },
      ),
    );
  }
}
