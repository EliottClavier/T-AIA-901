import 'package:flutter/material.dart';
import 'package:mobile/exception/ItinaryException.dart';
import 'package:mobile/services/PathRequestService.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

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
  PathRequestService pathRequestService = PathRequestService();

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
      body: Center(
        child: Container(
          padding: EdgeInsets.all(16.0),
          width: 300,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16.0),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.5),
                spreadRadius: 5,
                blurRadius: 7,
                offset: Offset(0, 3),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (_localeNames.isNotEmpty)
                DropdownButton<stt.LocaleName>(
                  value: _selectedLocale,
                  items: _localeNames.map((localeName) {
                    return DropdownMenuItem(
                      value: localeName,
                      child: Text(localeName.localeId),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      _selectedLocale = value;
                    });
                  },
                ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  IconButton(
                    iconSize: 40.0,
                    icon: const Icon(Icons.mic),
                    color: Colors.blue,
                    onPressed: _listen,
                  ),
                ],
              ),
              Expanded(
                child: TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: 'Parlez ou écrivez ici...',
                  ),
                  maxLines: null,
                  onChanged: (value) {
                    setState(() {
                      _text = value;
                    });
                  },
                  controller: TextEditingController(text: _text),
                ),
              ),
              SizedBox(height: 60),
              ElevatedButton(
                onPressed: () {
                  // Action de validation
                  pathRequestService.sendShortestPathRequest(_text);
                },
                child: Text('Valider'),
                style: ElevatedButton.styleFrom(
                  foregroundColor: Colors.white, backgroundColor: Colors.blue,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _listen() async {
    print("listening");
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
