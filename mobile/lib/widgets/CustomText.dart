import 'package:flutter/cupertino.dart';
import 'package:mobile/utils/AppColors.dart';

class CustomText extends StatelessWidget {
  final String text;
  final bool isUpperCase;
  final TextAlign textAlign;
  final String fontFamily;
  final FontWeight fontWeight;
  final double fontSize;
  final FontStyle fontStyle;
  final Color color;
  final Color? backgroundColor;

  CustomText({
    required this.text,
    this.isUpperCase = true,
    this.textAlign = TextAlign.center,
    this.fontFamily = 'SofiaSans',
    this.fontWeight = FontWeight.bold,
    this.fontSize = 17.0,
    this.fontStyle = FontStyle.normal,
    this.color = AppColors.whiteColor,
    this.backgroundColor = null,
  });

  @override
  Widget build(BuildContext context) {
    return Text(
      isUpperCase ? text.toUpperCase() : text,
      textAlign: textAlign,
      style: TextStyle(
        fontFamily: fontFamily,
        fontWeight: fontWeight,
        fontSize: fontSize,
        fontStyle: fontStyle,
        color: color,
        backgroundColor: backgroundColor ?? null,
      ),
    );
  }
}