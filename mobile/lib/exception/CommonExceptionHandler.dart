import 'package:flutter/material.dart';
import 'package:mobile/exception/CommonException.dart';
import 'package:mobile/exception/ItineraryException.dart';
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/utils/SnackBarUtils.dart';

class CommonExceptionHandler{

  static handleException(CommonException exception){
    if(exception is ItineraryException){
      _handleItineraryException(exception);
    } else {
      _handleCommonException(exception);
    }
  }

  static _handleCommonException(CommonException exception){
    SnackBarUtils.showSnackBar(exception.message, Colors.redAccent.shade400, 3).closed.then((value) => {
      NavigationService.backToVoiceRecognitionPage()
    });
  }

  static _handleItineraryException(ItineraryException exception){
    SnackBarUtils.showSnackBar(exception.message, Colors.deepOrange.shade400, 3).closed.then((value) => {
      NavigationService.backToVoiceRecognitionPage()
    });
  }
}