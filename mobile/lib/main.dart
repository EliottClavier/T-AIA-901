import 'dart:io';

import 'package:flutter/material.dart';
import 'package:mobile/exception/CommonException.dart';
import 'package:mobile/exception/CommonExceptionHandler.dart';
import 'widgets/VoiceRecognitionPage.dart';
import 'model/ItineraryResponse.dart';
import 'services/NavigationService.dart';

void main(){
  FlutterError.onError = (error) {
    if (error.exception is CommonException) {
      CommonExceptionHandler.handleException(error.exception as CommonException);
    } else if(error.exception is HttpException){
      CommonExceptionHandler.handleException(
          CommonException(
              "Http Exception",
              error.exception.toString()
          )
      );
    }
    else {
      FlutterError.presentError(error);
    }
  };
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {

    ItineraryResponse itineraryResponse = ItineraryResponse(
      sentenceID: "12345",
      departure: "Paris",
      destination: "Marseille",
      steps: ["Lyon", "Avignon"],
    );

    return MaterialApp(
      navigatorKey: NavigationService.navigatorKey,
      title: 'Voice Recognition App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: VoiceRecognitionPage(),
    );
  }
}