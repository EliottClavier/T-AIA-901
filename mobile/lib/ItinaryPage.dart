import 'package:flutter/material.dart';
import 'model/ItinaryResponse.dart';

class ItinaryPage extends StatelessWidget {
  final ItinaryResponse itinaryResponse;

  ItinaryPage({required this.itinaryResponse});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Itinéraire'),
      ),
      body: ListView.builder(
        itemCount: itinaryResponse.steps.length + 2,
        itemBuilder: (context, index) {
          if (index == 0) {
            return ListTile(title: Text('Départ: ${itinaryResponse.departure}'));
          } else if (index == itinaryResponse.steps.length + 1) {
            return ListTile(title: Text('Destination: ${itinaryResponse.destination}'));
          } else {
            return ListTile(title: Text('Étape ${index}: ${itinaryResponse.steps[index - 1]}'));
          }
        },
      ),
    );
  }
}
