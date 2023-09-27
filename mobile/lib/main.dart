import 'package:flutter/material.dart';
import 'package:mobile/exception/CommonException.dart';
import 'package:mobile/exception/CommonExceptionHandler.dart';
import 'widgets/VoiceRecognitionPage.dart';
import 'model/ItinaryResponse.dart';

void main(){
  FlutterError.onError = (error) {
    print(error);
    if (error.exception is CommonException) {
      CommonExceptionHandler.handleException(error.exception as CommonException);
    } else {
      FlutterError.presentError(error);
    }
  };
  runApp(MyApp());
}

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
      home: VoiceRecognitionPage(),
    );
  }
}