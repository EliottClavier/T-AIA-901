import 'package:flutter/material.dart';
import '../services/NavigationService.dart';


class SnackBarUtils{

  // Shows a snackbar with the given message and status
  static ScaffoldFeatureController<SnackBar, SnackBarClosedReason> showSnackBar(String message, Color backgroundColor, int duration) {
    BuildContext context = NavigationService.navigatorKey.currentContext!;
    return ScaffoldMessenger.of(context)
        .showSnackBar(_getSnackBar(message, backgroundColor, duration));
  }

// Returns a snackbar with the given message and status
  static SnackBar _getSnackBar(String message, Color backgroundColor, int duration) {

    return SnackBar(
      content: Text(
        message,
        style: const TextStyle(
          color: Colors.white,
        ),
      ),
      duration: Duration(seconds: duration),
      elevation: 25,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(8),
        ),
      ),
      backgroundColor: backgroundColor,
    );
  }
}