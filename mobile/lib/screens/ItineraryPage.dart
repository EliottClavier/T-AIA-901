import 'package:flutter/material.dart';
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/widgets/CustomText.dart';
import 'package:mobile/widgets/ItineraryComponent.dart';
import 'package:mobile/widgets/ItineraryComponentDot.dart';
import 'package:mobile/widgets/Wrapper.dart';
import '../model/ItineraryResponse.dart';
import '../utils/AppColors.dart';

class ItineraryPage extends StatelessWidget {
  final ItineraryResponse itineraryResponse;

  ItineraryPage({required this.itineraryResponse});

  String _getCurrentStep(int index) {
    if (index == 0) {
      return itineraryResponse.departure;
    } else if (index == itineraryResponse.steps.length + 1) {
      return itineraryResponse.destination;
    } else {
      return itineraryResponse.steps[index - 1];
    }
  }

  Widget _createEmptyContainer() {
    return Container(
        decoration: BoxDecoration(
          // No border
          border: Border.all(
            color: Colors.transparent,
            width: 0,
          ),
        )
    );
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
                  if (index == 0) ... [
                    AppBar(
                      backgroundColor: AppColors.backgroundColor,
                      elevation: 0,
                      title: CustomText(
                        text: "Back",
                        fontSize: 22.0,
                        fontWeight: FontWeight.w600,
                      ),
                      leading: IconButton(
                        icon: Icon(Icons.arrow_back),
                        iconSize: 40.0,
                        onPressed: () {
                          NavigationService.backToVoiceRecognitionPage();
                        },
                      )
                    ),
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
                  ],
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        flex: 2,
                        child: ItineraryComponentDot(
                          type: index == 0
                              ? ItineraryComponentDotType.departure
                              : index == itineraryResponse.steps.length + 1
                                  ? ItineraryComponentDotType.destination
                                  : ItineraryComponentDotType.step,
                        ),
                      ),
                      Expanded(
                        flex: 1,
                        child: _createEmptyContainer(),
                      ),
                      Expanded(
                        flex: 14,
                        child: ItineraryComponent(
                          text: "${_getCurrentStep(index)}",
                        ),
                      )
                    ],
                  ),
                  Row(
                    children: [
                      Expanded(
                        flex: 2,
                        child: index == itineraryResponse.steps.length + 1 ?
                        _createEmptyContainer() :
                        Container(
                          height: MediaQuery.of(context).size.height * 0.15,
                          color: AppColors.whiteColor,
                        ),
                      ),
                      Expanded(
                        flex: 1,
                        child: _createEmptyContainer(),
                      ),
                      Expanded(
                        flex: 14,
                        child: index == itineraryResponse.steps.length + 1 ?
                        _createEmptyContainer() :
                        Container(
                            height: MediaQuery.of(context).size.height * 0.15,
                            alignment: Alignment.centerLeft,
                            child: CustomText(
                              text: "_h__",
                            )
                        ),
                      )
                    ],
                  )
                ]
              );
            },
          ),
        )
      )
    );
  }
}
