import 'package:flutter/cupertino.dart';
import 'package:mobile/utils/AppColors.dart';

class CustomText extends StatelessWidget {
  final String text;
  final String fontFamily;
  final FontWeight fontWeight;
  final double fontSize;
  final Color color;
  final Color? backgroundColor;

  CustomText({
    required this.text,
    this.fontFamily = 'SofiaSans',
    this.fontWeight = FontWeight.bold,
    this.fontSize = 17.0,
    this.color = AppColors.whiteColor,
    this.backgroundColor = null,
  });

  @override
  Widget build(BuildContext context) {
    return Text(
      text.toUpperCase(),
      style: TextStyle(
        fontFamily: fontFamily,
        fontWeight: fontWeight,
        fontSize: fontSize,
        color: color,
        backgroundColor: backgroundColor ?? null,
      ),
    );
  }
}