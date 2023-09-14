import 'dart:convert';
import 'package:flutter/services.dart';

class Config {
  final String nlpApiUrl;

  Config._internal(this.nlpApiUrl);

  static Config? _instance;

  static Future<Config> getInstance() async {
    if (_instance == null) {
      final configString = await rootBundle.loadString('assets/config.json');
      final configJson = jsonDecode(configString);
      _instance = Config._internal(configJson['NLP_API_URL']);
    }
    return _instance!;
  }

  String getNlpApiUrl(){
    return this.nlpApiUrl;
  }
}
