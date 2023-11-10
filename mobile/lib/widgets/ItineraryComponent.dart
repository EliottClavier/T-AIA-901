import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../utils/AppColors.dart';
import 'CustomText.dart';

class ItineraryComponent extends StatelessWidget {

  final String text;
  final String prependText;
  final double size;

  ItineraryComponent({required this.text, this.prependText = "", this.size = 50.0});

  @override
  Widget build(BuildContext context) {
    return Container(
        padding: EdgeInsets.symmetric(horizontal: 22.0),
        height: size,
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
                fontWeight: FontWeight.w700,
                color: AppColors.greyColor,
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