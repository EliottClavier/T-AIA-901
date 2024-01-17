import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/config/Config.dart';
import 'package:mobile/model/ItineraryResponse.dart';

import '../exception/ItineraryException.dart';
import '../exception/enums/ItinaryExceptionEnumCode.dart';

class ItineraryService {

  late ItineraryResponse itineraryResponse;

  late String API_URL;

  ItineraryService(){
    Config.getInstance().then((config) {
      API_URL = config.getApiUrl();
    });
  }

  askItineraryFromInputText(String input) async {
    NavigationService.navigateToLoadingScreen();
    sendItineraryRequest(input);
  }

  sendItineraryRequest(String input) async {
    final response = await http.post(
      Uri.parse(API_URL),
      body: jsonEncode(input),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      try{
        this.itineraryResponse = ItineraryResponse.fromJson(jsonDecode(response.body));
        NavigationService.navigateToItineraryPage(itineraryResponse);
      } catch (e) {
        throw ItineraryException("Error while parsing the response", e.toString());
      }
    } else {
      String sentenceId = jsonDecode(response.body)["sentenceId"] ?? null;
      throw ItineraryException.createFromEnumCode(
          ItineraryExceptionEnumCode.fromCode(jsonDecode(response.body)["code"]), sentenceId
      );
    }
  }

}