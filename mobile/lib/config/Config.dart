import 'dart:convert';
import 'package:flutter/services.dart';

class Config {
  final String apiUrl;

  Config._internal(this.apiUrl);

  static Config? _instance;

  static Future<Config> getInstance() async {
    if (_instance == null) {
      final configString = await rootBundle.loadString('config/config.json');
      final configJson = jsonDecode(configString);
      _instance = Config._internal(configJson['API_URL']);
    }
    return _instance!;
  }

  String getApiUrl(){
    return this.apiUrl;
  }
}
