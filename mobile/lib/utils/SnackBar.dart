import 'package:flutter/material.dart';

import '../services/NavigationService.dart';


// Shows a snackbar with the given message and status
void showSnackBar(String message, String status, int duration) {
  BuildContext context = NavigationService.navigatorKey.currentContext!;
  ScaffoldMessenger.of(context)
      .showSnackBar(getSnackBar(message, status, duration));
}

// Returns a snackbar with the given message and status
SnackBar getSnackBar(String message, String status, int duration) {
  Color backgroundColor = getBackgroundColor(status);

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

// Returns the background color of the snackbar based on the status
Color getBackgroundColor(String status) {
  if (status == "success") {
    return Colors.teal.shade700;
  } else if (status == "error") {
    return Colors.redAccent.shade400;
  } else {
    return Colors.indigoAccent.shade700;
  }
}