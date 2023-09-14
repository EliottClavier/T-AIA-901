import 'dart:convert';
import 'package:http/http.dart' as http;
import '../model/ShortestPathResponse.dart';
import '../config/Config.dart';

class PathRequestService {

  late ShortestPathResponse shortestPathResponse;

  late String NLP_API_URL;

  PathRequestService(){
    Config.getInstance().then((config) =>
      NLP_API_URL = config.getNlpApiUrl()
    );
  }

  sendShortestPathRequest(String input) async {
    final response = await http.post(
      Uri.parse(NLP_API_URL),
      body: jsonEncode(input),
      headers: {
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      this.shortestPathResponse = ShortestPathResponse.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to find path');
    }
  }
}