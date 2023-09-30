import 'package:flutter/material.dart';
import 'package:mobile/services/ItineraryService.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

import '../utils/AppColors.dart';

class VoiceRecognitionPage extends StatefulWidget {
  @override
  _VoiceRecognitionPageState createState() => _VoiceRecognitionPageState();
}

class _VoiceRecognitionPageState extends State<VoiceRecognitionPage> {
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = '';
  List<stt.LocaleName> _localeNames = [];
  stt.LocaleName? _selectedLocale;
  ItineraryService itineraryService = ItineraryService();

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initializeSpeech();
  }

  void _initializeSpeech() async {
    bool available = await _speech.initialize();
    if (available) {
      _localeNames = await _speech.locales();
      setState(() {
        _selectedLocale = _localeNames.first;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
          padding: EdgeInsets.all(30.0),
          constraints: BoxConstraints(
            minHeight: MediaQuery.of(context).size.height * 1,
          ),
          width: MediaQuery.of(context).size.width * 1,
          decoration: BoxDecoration(
            color: AppColors.backgroundColor,
          ),
          child: Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: CustomText(
                    text: "Hi !",
                    fontWeight: FontWeight.w600,
                  ),
                ),
                SizedBox(height: 10),
                Align(
                  alignment: Alignment.centerLeft,
                  child: CustomText(
                    text: "Tell us about your travelling desires.",
                    fontWeight: FontWeight.w700,
                  ),
                ),
                SizedBox(height: 50),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Container(
                      decoration: BoxDecoration(
                        color: AppColors.primaryColor,
                        borderRadius: BorderRadius.circular(80.0),
                      ),
                      child: IconButton(
                        iconSize: 50.0,
                        padding: EdgeInsets.all(25.0),
                        icon: const Icon(Icons.mic),
                        color: AppColors.whiteColor,
                        onPressed: _listen,
                      ),
                    )
                  ],
                ),
                SizedBox(height: 30),
                //if (_localeNames.isNotEmpty)
                  Column(
                    children: [
                      Container(
                          width: MediaQuery.of(context).size.width * 0.8,
                          padding: EdgeInsets.symmetric(horizontal: 22.0),
                          decoration: BoxDecoration(
                            color: AppColors.primaryColor,
                            borderRadius: BorderRadius.circular(4.0),
                          ),
                          child: DropdownButtonHideUnderline(
                            child: DropdownButton<stt.LocaleName>(
                              isExpanded: true,
                              borderRadius: BorderRadius.circular(4.0),
                              focusColor: AppColors.primaryColor,
                              hint: Center(
                                child: CustomText(
                                  text: 'Select a language',
                                ),
                              ),
                              icon: Icon(
                                Icons.arrow_drop_down,
                                color: AppColors.whiteColor,
                              ),
                              value: _selectedLocale,
                              items: _localeNames.map((localeName) {
                                return DropdownMenuItem(
                                    value: localeName,
                                    child: Center(
                                      child: CustomText(
                                          text: localeName.name,
                                          color: Colors.black
                                      ),
                                    )
                                );
                              }).toList(),
                              onChanged: (value) {
                                setState(() {
                                  _selectedLocale = value;
                                });
                              },
                            ),
                          )
                      ),
                      SizedBox(height: 50),
                    ],
                  ),
                Container(
                  width: MediaQuery.of(context).size.width * 0.8,
                  child: Divider(
                    color: AppColors.whiteColor,
                    thickness: 1,
                  ),
                ),
                SizedBox(height: 50),
                SizedBox(
                    width: MediaQuery.of(context).size.width * 0.8,
                    child: Container(
                      child: TextField(
                        style: TextStyle(
                          fontFamily: 'SofiaSans',
                          fontWeight: FontWeight.bold,
                          color: AppColors.whiteColor,
                        ),
                        decoration: InputDecoration(
                            filled: true,
                            fillColor: AppColors.secondaryColor,
                            contentPadding: EdgeInsets.symmetric(horizontal: 22.0, vertical: 15.0),
                            enabledBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(4.0)
                            ),
                            hintText: 'Commande textuelle'.toUpperCase(),
                            hintStyle: TextStyle(
                                color: AppColors.whiteColor,
                                fontFamily: 'SofiaSans',
                                fontSize: 17.0,
                                fontWeight: FontWeight.bold
                            ),
                            suffixIcon: IconButton(
                              icon: Icon(Icons.send),
                              onPressed: () {
                                itineraryService.askItineraryFromInputText(_text);
                              },
                            ),
                            suffixIconColor: AppColors.whiteColor
                        ),
                        maxLines: 1,
                        onChanged: (value) {
                          setState(() {
                            _text = value;
                          });
                        },
                        controller: TextEditingController(text: _text),
                      ),
                    )
                ),
              ],
            ),
          )
      ),
    );
  }

  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) => setState(() => _isListening = val == 'listening'),
      );
      if (available) {
        _speech.listen(
          onResult: (val) => setState(() => _text = val.recognizedWords),
          localeId: _selectedLocale?.localeId,
        );
      }
    } else {
      _speech.stop();
      setState(() => _isListening = false);
    }
  }
}
