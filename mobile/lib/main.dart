import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mobile/exception/CommonException.dart';
import 'package:mobile/exception/CommonExceptionHandler.dart';
import 'package:mobile/screens/SplashScreen.dart';
import 'package:mobile/screens/VoiceRecognitionPage.dart';
import 'package:mobile/utils/AppColors.dart';
import 'services/NavigationService.dart';

void main(){
  SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
    statusBarColor: AppColors.backgroundColor,
    systemNavigationBarColor: AppColors.backgroundColor,
  ));

  FlutterError.onError = (error) {
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

    return MaterialApp(
      navigatorKey: NavigationService.navigatorKey,
      title: 'Voice Recognition App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: SplashScreen()
    );
  }
}