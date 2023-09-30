import 'package:flutter/material.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:mobile/widgets/ItineraryComponent.dart';
import 'package:mobile/widgets/Wrapper.dart';
import '../model/ItineraryResponse.dart';
import '../utils/AppColors.dart';

class ItineraryPage extends StatelessWidget {
  final ItineraryResponse itineraryResponse;

  ItineraryPage({required this.itineraryResponse});

  String getCurrentStep(int index) {
    if (index == 0) {
      return itineraryResponse.departure;
    } else if (index == itineraryResponse.steps.length + 1) {
      return itineraryResponse.destination;
    } else {
      return itineraryResponse.steps[index - 1];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Wrapper(
        child: Container(
          padding: EdgeInsets.all(30.0),
          child: ListView.builder(
            itemCount: itineraryResponse.steps.length + 2,
            itemBuilder: (context, index) {
              return Column(
                children: [
                  if (index == 0)
                    Container(
                      width: MediaQuery.of(context).size.width * 0.8,
                      child: Column(
                        mainAxisSize: MainAxisSize.max,
                        children: [
                          Divider(
                            color: AppColors.whiteColor,
                            thickness: 1,
                            height: 40,
                          ),
                          ItineraryComponent(
                            prependText: "Departure : ",
                            text: " ${itineraryResponse.departure}",
                          ),
                          SizedBox(height: 15.0),
                          ItineraryComponent(
                            prependText: "Arrival : ",
                            text: " ${itineraryResponse.destination}",
                          ),
                          Divider(
                            color: AppColors.whiteColor,
                            thickness: 1,
                            height: 40,
                          ),
                          ItineraryComponent(
                            prependText: "Total time : ",
                            text: "",
                          ),
                          SizedBox(height: 30.0),
                          CustomText(
                            text: "Your trip summary",
                            fontSize: 22.0,
                          ),
                          SizedBox(height: 30.0)
                        ],
                      ),
                    ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        flex: 1,
                        child: Column(
                          children: [
                            Container(
                              width: 40.0,
                              height: 40.0,
                              decoration: BoxDecoration(
                                color: AppColors.whiteColor,
                                shape: BoxShape.circle,
                              ),
                              child: Container(
                                margin: EdgeInsets.all(5.0),
                                decoration: BoxDecoration(
                                  color: AppColors.backgroundColor,
                                  shape: BoxShape.circle,
                                ),
                              ),
                            ),

                            if (index != itineraryResponse.steps.length + 1)
                              Container(
                                width: 5.0,
                                height: 60.0,
                                color: AppColors.whiteColor,
                              ),
                          ],
                        )
                      ),
                      Expanded(
                        flex: 5,
                        child: ItineraryComponent(
                          text: "${getCurrentStep(index)}",
                        ),
                      )
                    ],
                  ),
                ]
              );
            },
          ),
        )

      )
    );
  }
}
