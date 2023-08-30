import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class VoiceRecognitionPage extends StatefulWidget {
  @override
  _VoiceRecognitionPageState createState() => _VoiceRecognitionPageState();
}

class _VoiceRecognitionPageState extends State<VoiceRecognitionPage> {
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = '';

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton(
            onPressed: _listen,
            child: Icon(Icons.mic, size: 40),
            style: ElevatedButton.styleFrom(
              shape: CircleBorder(),
              padding: EdgeInsets.all(24),
              primary: Colors.blue,
              onPrimary: Colors.white,
            ),
          ),
          SizedBox(height: 30),
          Expanded(
            child: SingleChildScrollView(
              reverse: true,
              child: Text(
                _text,
                style: TextStyle(fontSize: 20),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _listen() async {
    print("listnening...");
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) => setState(() => _isListening = val == 'listening'),
      );
      if (available) {
        print("available");
        _speech.listen(
          onResult: (val) => setState(() {
            print(val);
            _text = val.recognizedWords;
          }),
        );
      }
    } else {
      _speech.stop();
      setState(() => _isListening = false);
    }
  }
}
