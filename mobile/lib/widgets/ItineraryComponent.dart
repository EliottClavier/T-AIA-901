import 'package:flutter/cupertino.dart';

import '../utils/AppColors.dart';
import 'CustomText.dart';

class ItineraryComponent extends StatelessWidget {

  final String text;
  final String prependText;

  ItineraryComponent({required this.text, this.prependText = ""});

  @override
  Widget build(BuildContext context) {
    return Container(
        padding: EdgeInsets.symmetric(horizontal: 22.0, vertical: 15.0),
        decoration: BoxDecoration(
          color: AppColors.secondaryColor,
          borderRadius: BorderRadius.circular(4.0),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            if (prependText.isNotEmpty)
              CustomText(
                text: prependText,
                isUpperCase: false,
                fontWeight: FontWeight.w600,
                color: AppColors.darkGreyColor,
              ),
            CustomText(
              text: text,
              isUpperCase: false,
              fontWeight: FontWeight.w600,
            ),
          ],
        )
    );
  }

}