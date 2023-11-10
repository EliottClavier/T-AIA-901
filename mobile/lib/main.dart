import 'package:flutter/material.dart';
import 'VoiceRecognitionPage.dart';
import 'ItinaryPage.dart';
import 'model/ItinaryResponse.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {

    ItinaryResponse itinaryResponse = ItinaryResponse(
      sentenceID: "12345",
      departure: "Paris",
      destination: "Marseille",
      steps: ["Lyon", "Avignon"],
    );

    return MaterialApp(
      title: 'Voice Recognition App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ItinaryPage(itinaryResponse: itinaryResponse),
    );
  }
}