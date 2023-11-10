import 'package:animate_do/animate_do.dart';
import 'package:dotlottie_loader/dotlottie_loader.dart';
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:mobile/services/NavigationService.dart';
import 'package:mobile/widgets/Wrapper.dart';

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with TickerProviderStateMixin {

  bool _screenVisible = true;

  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(vsync: this);

    Future.delayed(Duration(milliseconds: 2500), () {
      setState(() {
        _screenVisible = false;
      });
      Future.delayed(Duration(milliseconds: 400), () {
        NavigationService.navigateToVoiceRecognitionPage();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Hero(
          tag: "splashScreen",
          child: Wrapper(
              child: Container(
                  padding: EdgeInsets.all(30.0),
                  child: AnimatedOpacity(
                    opacity: _screenVisible ? 1.0 : 0.0,
                    duration: Duration(milliseconds: 700),
                    child: ZoomIn(
                      duration: Duration(milliseconds: 700),
                      child: ZoomOut(
                        animate: !_screenVisible,
                        duration: Duration(milliseconds: 400),
                        child: DotLottieLoader.fromAsset("assets/images/train.lottie",
                            frameBuilder: (BuildContext ctx, DotLottie? dotlottie) {
                              if (dotlottie != null) {
                                return Lottie.memory(
                                  dotlottie.animations.values.single,
                                  frameRate: FrameRate(60),
                                  controller: _controller,
                                  onLoaded: (composition) {
                                    Future.delayed(Duration(milliseconds: 700), () {
                                      _controller
                                        ..duration = Duration(milliseconds: 1100)
                                        ..forward();
                                    });
                                  },
                                );
                              } else {
                                return Container();
                              }
                            }
                        ),
                      )
                    ),
                  )
              )
          ),
        )
     );
  }
}
