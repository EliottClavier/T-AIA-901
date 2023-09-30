import 'package:flutter/cupertino.dart';

import '../utils/AppColors.dart';

class Wrapper extends StatelessWidget {

  final Widget child;

  Wrapper({required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: MediaQuery.of(context).size.width * 1,
      height: MediaQuery.of(context).size.height * 1,
      decoration: BoxDecoration(
      color: AppColors.backgroundColor,
      ),
      child: child,
    );
  }

}