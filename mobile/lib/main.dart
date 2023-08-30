import 'package:flutter/material.dart';
import 'VoiceRecognitionPage.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice Recognition App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: VoiceRecognitionPage(), // Définissez VoiceRecognitionPage comme page d'accueil
    );
  }
}