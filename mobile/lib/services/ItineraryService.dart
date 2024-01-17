import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/config/Config.dart';
import 'package:mobile/model/ItineraryResponse.dart';
import 'package:mobile/utils/SnackBarUtils.dart';

import '../exception/ItineraryException.dart';
import '../exception/enums/ItinaryExceptionEnumCode.dart';

class ItineraryService {

  late String API_URL;

  ItineraryService(){
    Config.getInstance().then((config) {
      API_URL = config.getApiUrl();
    });
  }

  askItineraryFromInputText(String input) async {
    sendItineraryRequest(input);
    NavigationService.navigateToLoadingScreen();
  }

  sendItineraryRequest(String input) async {
    final response = await http.post(
      Uri.parse(this.API_URL + "trip/details/"),
      body: jsonEncode({
        "sentence": input,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    ItineraryResponse itineraryResponse = ItineraryResponse.fromJson(jsonDecode(response.body));

    if (response.statusCode == 200 && itineraryResponse.state == "CORRECT") {
      NavigationService.navigateToItineraryPage(itineraryResponse);
    } else {
      NavigationService.backToVoiceRecognitionPage();
      SnackBarUtils.showSnackBar(
          ItineraryException.createFromEnumCode(
              ItineraryExceptionEnumCode.fromCode(itineraryResponse.state)
          ).message,
          Colors.red,
          5
      );
    }
  }

}