import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/config/Config.dart';
import 'package:mobile/model/ItineraryResponse.dart';

import '../exception/ItineraryException.dart';

class ItineraryService {

  late ItineraryResponse itineraryResponse;

  late String NLP_API_URL;

  ItineraryService(){
    Config.getInstance().then((config) {
      NLP_API_URL = config.getNlpApiUrl();
    });
  }

  askItineraryFromInputText(String input) async {
    NavigationService.navigateToLoadingScreen();
    sendItineraryRequest(input);
  }

  sendItineraryRequest(String input) async {
    final response = await http.post(
      Uri.parse(NLP_API_URL),
      body: jsonEncode(input),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      this.itineraryResponse = ItineraryResponse.fromJson(jsonDecode(response.body));
      NavigationService.navigateToItineraryPage(itineraryResponse);
    } else {
      throw ItineraryException("Error", "Error while sending request to NLP API");
    }
  }
}