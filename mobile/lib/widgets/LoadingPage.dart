import 'package:flutter/material.dart';
import '../model/ItinaryResponse.dart';

class LoadingPage extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Loading'),
      ),
      body: CircularProgressIndicator()
    );
  }
}
