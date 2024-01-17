import 'package:flutter/material.dart';
import 'package:mobile/model/TripStep.dart';
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

  String _minutesToHHMM(int minutes) {
    Duration duration = Duration(minutes: minutes);
    int hours = duration.inHours;
    int remainingMinutes = duration.inMinutes.remainder(60);

    String formattedTime = '${hours.toString().padLeft(2, '0')}h${remainingMinutes.toString().padLeft(2, '0')}';

    return formattedTime;
  }

  int _getTotalDuration() {
    int totalDuration = 0;
    itineraryResponse.steps!.forEach((step) {
      step.duration_between_stations.forEach((duration) {
        if (duration != null) {
          totalDuration += duration;
        }
      });
    });
    return totalDuration;
  }

  Container _createEmptyContainer() {
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

  List<Widget> _getListHeader(BuildContext context) {
    return [
      AppBar(
          backgroundColor: AppColors.backgroundColor,
          elevation: 0,
          title: CustomText(
            text: "Retour",
            fontSize: 22.0,
            fontWeight: FontWeight.w600,
          ),
          leading: IconButton(
            icon: Icon(Icons.arrow_back, color: AppColors.whiteColor),
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
              prependText: "Départ : ",
              text: " ${itineraryResponse.steps![0].departure}",
            ),
            SizedBox(height: 15.0),
            ItineraryComponent(
              prependText: "Arrivée : ",
              text: " ${itineraryResponse.steps![itineraryResponse.steps!.length - 1].arrival}",
            ),
            Divider(
              color: AppColors.whiteColor,
              thickness: 1,
              height: 40,
            ),
            ItineraryComponent(
              prependText: "Durée totale : ",
              text: " ${_minutesToHHMM(_getTotalDuration())}",
            ),
            SizedBox(height: 30.0),
            CustomText(
              text: "Résume de votre voyage",
              fontSize: 22.0,
            ),
            SizedBox(height: 30.0)
          ],
        ),
      )
    ];
  }

  Row _getDotRow(BuildContext context, int index, int length, String city) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          flex: 2,
          child: ItineraryComponentDot(
            type: index == 0
                ? ItineraryComponentDotType.departure
                : index + 1 == length
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
            text: city,
          ),
        )
      ],
    );
  }

  Row _getLineRow(BuildContext context, int index, int length, int? duration) {
    return Row(
      children: [
        Expanded(
          flex: 2,
          child: index + 1 == length ?
          _createEmptyContainer() :
          Container(
            height: MediaQuery.of(context).size.height * 0.15,
            decoration: BoxDecoration(
              color: AppColors.whiteColor,
              border: Border.all(
                color: AppColors.whiteColor,
                width: 0.0,
              ),
            ),
          ),
        ),
        Expanded(
          flex: 1,
          child: _createEmptyContainer(),
        ),
        Expanded(
          flex: 14,
          child: index + 1 == length ?
          _createEmptyContainer() :
          Container(
              height: MediaQuery.of(context).size.height * 0.15,
              alignment: Alignment.centerLeft,
              child: CustomText(
                text: duration != null ? _minutesToHHMM(duration) : "_h__",
              )
          ),
        )
      ],
    );
  }

  Column _getRow(BuildContext context, TripStep step) {
    return Column(
      children: step.path.asMap().entries.map((entry) => [
        _getDotRow(context, entry.key, step.path.length, entry.value),
        _getLineRow(context, entry.key, step.path.length, step.duration_between_stations[entry.key])
      ]).expand((element) => element).toList(),
    );
  }

  ListView _getListView() {
    return ListView.builder(
      itemCount: itineraryResponse.steps!.length,
      itemBuilder: (context, index) {
        return Padding(
            padding: EdgeInsets.only(bottom: 30.0),
            child: Column(
                children: [
                  if (index == 0) ... _getListHeader(context),
                  if (itineraryResponse.steps!.length > 1) Padding(
                      padding: EdgeInsets.only(bottom: 30.0),
                      child: CustomText(
                        text: "Etape ${index + 1}",
                        fontSize: 22.0,
                      )
                  ),
                  _getRow(context, itineraryResponse.steps![index]),
                ]
            )
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Wrapper(
        child: Container(
          padding: EdgeInsets.all(30.0),
          child: _getListView(),
        )
      )
    );
  }
}
