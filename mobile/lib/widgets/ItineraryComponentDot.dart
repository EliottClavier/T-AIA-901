
import 'package:flutter/cupertino.dart';

import '../utils/AppColors.dart';

enum ItineraryComponentDotType {
  departure,
  destination,
  step,
}

class ItineraryComponentDot extends StatelessWidget {

  final ItineraryComponentDotType type;
  final double size;

  ItineraryComponentDot({required this.type, this.size = 50.0});

  _getBorderRadiusByType() {
    switch (type) {
      case ItineraryComponentDotType.departure:
        return BorderRadius.only(
          topLeft: Radius.circular(20.0),
          topRight: Radius.circular(20.0),
        );
      case ItineraryComponentDotType.destination:
        return BorderRadius.only(
          bottomLeft: Radius.circular(20.0),
          bottomRight: Radius.circular(20.0),
        );
      case ItineraryComponentDotType.step:
        return BorderRadius.circular(0);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            color: AppColors.whiteColor,
            shape: BoxShape.circle,
          ),
          child: Container(
            padding: EdgeInsets.all(3.5),
            decoration: BoxDecoration(
              color: AppColors.whiteColor,
              borderRadius: _getBorderRadiusByType(),
              border: Border.all(
                color: AppColors.whiteColor,
                width: 0.0,
              ),
            ),
            child: Container(
              decoration: BoxDecoration(
                color: AppColors.backgroundColor,
                shape: BoxShape.circle,
              ),
            ),
          ),
        ),
      ],
    );
  }
}