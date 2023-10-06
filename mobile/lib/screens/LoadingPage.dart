import 'package:flutter/material.dart';
import 'package:mobile/model/ItineraryResponse.dart';
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/utils/AppColors.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:mobile/widgets/Wrapper.dart';

class LoadingPage extends StatelessWidget {

  LoadingPage() {
    Future.delayed(Duration(seconds: 3), () {
      ItineraryResponse itineraryResponse = ItineraryResponse(
        sentenceID: "12345",
        departure: "Paris",
        destination: "Marseille",
        steps: ["Lyon", "Avignon"],
      );
      NavigationService.navigateToItineraryPage(itineraryResponse);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Wrapper(
        child: Container(
          padding: EdgeInsets.all(30.0),
          child: Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                CircularProgressIndicator(
                  color: AppColors.whiteColor,
                  backgroundColor: AppColors.secondaryColor,
                  strokeWidth: 7.0,
                  strokeAlign: 5,
                ),
                SizedBox(height: 60),
                CustomText(
                    text: "Chargement",
                    fontSize: 30.0,
                ),
                SizedBox(height: 20),
                CustomText(
                  text: "Nous recherchons pour vous le chemin le plus court",
                  fontWeight: FontWeight.w600,
                  fontStyle: FontStyle.italic,
                ),
              ],
            )
          ),
        )
      )
    );
  }
}
