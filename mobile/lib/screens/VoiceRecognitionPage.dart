import 'package:avatar_glow/avatar_glow.dart';
import 'package:flutter/material.dart';
import 'package:mobile/services/ItineraryService.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:mobile/widgets/Wrapper.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

import '../utils/AppColors.dart';

class VoiceRecognitionPage extends StatefulWidget {
  @override
  _VoiceRecognitionPageState createState() => _VoiceRecognitionPageState();
}

class _VoiceRecognitionPageState extends State<VoiceRecognitionPage> {
  late stt.SpeechToText _speech;
  String _text = '';
  List<stt.LocaleName> _localeNames = [];
  stt.LocaleName? _selectedLocale;
  ItineraryService itineraryService = ItineraryService();

  final TextEditingController _textEditingController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initializeSpeech();
  }

  void _initializeSpeech() async {
    bool available = await _speech.initialize(
        onError: (errorNotification) {
          _stopListening();
        }
    );
    if (available) {
      _localeNames = await _speech.locales();
      setState(() {
        _selectedLocale = _localeNames.firstWhere(
            (localeName) => localeName.localeId == 'fr_FR',
            orElse: () => _localeNames.first
        );
      });
    }
  }

  void _onClear() {
    if (_text.isNotEmpty) {
      setState(() {
        _text = '';
      });
      _textEditingController.clear();
    }
  }

  void _onSend() {
    if (_text.isNotEmpty) {
      itineraryService.askItineraryFromInputText(_text);
      FocusManager.instance.primaryFocus?.unfocus();
    }
  }

  void _listen() async {
    bool available = await _speech.initialize();
    if (available) {
      await _speech.listen(
        onResult: _onSpeechResult,
        localeId: _selectedLocale?.localeId,
      );
      setState(() {});
    }
  }

  void _onSpeechResult(SpeechRecognitionResult result) {
    setState(() {
      _text = result.recognizedWords;
      _textEditingController.text = _text;
    });
  }

  void _stopListening() {
    _speech.stop();
    setState(() {});
  }

  Container _getTitle() {
    return Container(
      margin: EdgeInsets.only(bottom: 10.0),
      child: Align(
        alignment: Alignment.centerLeft,
        child: CustomText(
          text: "Bonjour !",
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }

  Container _getSubtitle() {
    return Container(
      margin: EdgeInsets.only(bottom: 50.0),
      child: Align(
        alignment: Alignment.centerLeft,
        child: CustomText(
          text: "Parlez-nous de vos envies de voyage.",
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }

  Container _getMicButton() {
    return Container(
      margin: EdgeInsets.only(bottom: 30.0),
      child: AvatarGlow(
        glowColor: AppColors.primaryColor,
        endRadius: 90.0,
        duration: Duration(milliseconds: 2000),
        repeat: true,
        showTwoGlows: true,
        repeatPauseDuration: Duration(milliseconds: 100),
        child: Container(
          decoration: BoxDecoration(
            color: _speech.isListening ? AppColors.secondaryColor : AppColors.primaryColor,
            borderRadius: BorderRadius.circular(80.0),
          ),
          child: IconButton(
            iconSize: 50.0,
            padding: EdgeInsets.all(25.0),
            icon: const Icon(Icons.mic),
            color: AppColors.whiteColor,
            disabledColor: AppColors.greyColor,
            onPressed: _speech.isListening ? _stopListening : _listen,
          ),
        ),
      )
    );
  }

  Column _getLocalesDropdown() {
    return Column(
      children: [
        Container(
            padding: EdgeInsets.symmetric(horizontal: 22.0),
            decoration: BoxDecoration(
              color: AppColors.primaryColor,
              borderRadius: BorderRadius.circular(4.0),
            ),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<stt.LocaleName>(
                dropdownColor: AppColors.secondaryColor,
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
                            color: AppColors.whiteColor
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
      ],
    );
  }

  Divider _getDivider() {
    return Divider(
      color: AppColors.whiteColor,
      thickness: 1,
      height: 120,
    );
  }

  TextField _getTextInput() {
    return TextField(
      maxLines: null,
      keyboardType: TextInputType.multiline,
      style: TextStyle(
        fontFamily: 'SofiaSans',
        fontWeight: FontWeight.bold,
        color: AppColors.whiteColor,
      ),
      onChanged: (value) {
        setState(() {
          _text = value;
        });
      },
      controller: _textEditingController,
      decoration: InputDecoration(
          filled: true,
          fillColor: AppColors.secondaryColor,
          contentPadding: EdgeInsets.symmetric(horizontal: 22.0, vertical: 15.0),
          enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(4.0)
          ),
          focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(
                  color: AppColors.greyColor,
                  width: 2.0
              )
          ),
          hintText: 'Commande textuelle'.toUpperCase(),
          hintStyle: TextStyle(
              color: AppColors.greyColor,
              fontFamily: 'SofiaSans',
              fontSize: 17.0,
              fontWeight: FontWeight.bold
          ),
          prefixIcon: _text.isNotEmpty ? IconButton(
            icon: Icon(Icons.clear),
            onPressed: _onClear,
          ) : null,
          prefixIconColor: Colors.red,
          suffixIcon: IconButton(
            icon: Icon(Icons.send),
            onPressed: _textEditingController.text.isNotEmpty ? _onSend : null,
            disabledColor: AppColors.greyColor,
          ),
          suffixIconColor: AppColors.whiteColor
      ),
    );
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: Wrapper(
        child: SingleChildScrollView(
          child: Container(
              padding: EdgeInsets.symmetric(
                  horizontal: 30.0,
                  vertical: 30.0 + MediaQuery.of(context).viewInsets.bottom / 4
              ),
              constraints: BoxConstraints(
                minHeight: MediaQuery.of(context).size.height * 1,
              ),
              decoration: BoxDecoration(
                color: AppColors.backgroundColor,
              ),
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _getTitle(),
                    _getSubtitle(),
                    _getMicButton(),
                    if (_localeNames.isNotEmpty)
                      _getLocalesDropdown(),
                    _getDivider(),
                    _getTextInput(),
                  ],
                ),
              )
          ),
        )
      )
    );
  }
}
