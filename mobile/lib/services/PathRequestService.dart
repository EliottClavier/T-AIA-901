import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mobile/services/NavigationService.dart';
import '../config/Config.dart';
import '../model/ItinaryResponse.dart';
import '../widgets/LoadingPage.dart';

class PathRequestService {

  late ItinaryResponse itinaryResponse;

  late String NLP_API_URL;

  PathRequestService(){
    Config.getInstance().then((config) =>
      NLP_API_URL = config.getNlpApiUrl()
    );
    print("Config API URL : ${NLP_API_URL}");
  }

  sendShortestPathRequest(String input) async {
    BuildContext context = NavigationService.navigatorKey.currentContext!;
    navigateToLoadingScreen(context);

    final response = await http.post(
      Uri.parse(NLP_API_URL),
      body: jsonEncode(input),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      this.itinaryResponse = ItinaryResponse.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to find path');
    }
  }

  navigateToLoadingScreen(BuildContext context){
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => LoadingPage(),
    )
    );
  }
}