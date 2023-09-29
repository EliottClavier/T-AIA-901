import 'package:flutter/material.dart';
import 'package:mobile/model/ItineraryResponse.dart';
import 'package:mobile/widgets/ItineraryPage.dart';
import 'package:mobile/widgets/VoiceRecognitionPage.dart';

import '../widgets/LoadingPage.dart';

class NavigationService {
  static GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
  static BuildContext get context => navigatorKey.currentContext!;

  static Future<dynamic> navigateToLoadingScreen() {
    return Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => LoadingPage(),
    )
    );
  }

  static Future<dynamic> navigateToVoiceRecognitionPage() {
    return Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => VoiceRecognitionPage(),
    )
    );
  }

  static Future<dynamic> navigateToItineraryPage(ItineraryResponse itineraryResponse) {
    return Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => ItineraryPage(itineraryResponse: itineraryResponse),
    )
    );
  }

  static void backToVoiceRecognitionPage() {
    return Navigator.of(context).popUntil((route) => route.isFirst);
  }

}