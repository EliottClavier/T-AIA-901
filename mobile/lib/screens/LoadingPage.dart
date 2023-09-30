import 'package:flutter/material.dart';
import 'package:mobile/utils/AppColors.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:mobile/widgets/Wrapper.dart';

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
                  CircularProgressIndicator(
                    color: AppColors.whiteColor,
                    backgroundColor: AppColors.secondaryColor,
                    strokeWidth: 7.0,
                    strokeAlign: 5,
                  ),
                  SizedBox(height: 60),
                  CustomText(
                      text: "Processing",
                      fontSize: 30.0,
                  ),
                  SizedBox(height: 20),
                  CustomText(
                    text: "We are searching for the shortest path",
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
