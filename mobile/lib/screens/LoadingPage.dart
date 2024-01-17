import 'package:flutter/material.dart';
import 'package:mobile/model/ItineraryResponse.dart';
import 'package:mobile/services/ItineraryService.dart';
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/utils/AppColors.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:mobile/widgets/Wrapper.dart';

import '../model/TripStep.dart';

class LoadingPage extends StatelessWidget {

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
                Container(
                  margin: EdgeInsets.only(bottom: 60.0),
                  child: CircularProgressIndicator(
                    color: AppColors.whiteColor,
                    backgroundColor: AppColors.secondaryColor,
                    strokeWidth: 7.0,
                    strokeAlign: 5,
                  ),
                ),
                Container(
                  margin: EdgeInsets.only(bottom: 20.0),
                  child: CustomText(
                    text: "Chargement",
                    fontSize: 30.0,
                  ),
                ),
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
