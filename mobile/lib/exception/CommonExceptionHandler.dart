import 'package:mobile/exception/CommonException.dart';
import 'package:mobile/exception/ItinaryException.dart';
import 'package:mobile/utils/SnackBar.dart';

class CommonExceptionHandler{

  static handleException(CommonException exception){
    if(exception is ItinaryException){
      _handleItinaryException(exception);
    } else {
      _handleCommonException(exception);
    }
  }

  static _handleCommonException(CommonException exception){
    print("Common Exception occured");
  }

  static _handleItinaryException(ItinaryException exception){
    print("Itinary Exception occured");
    showSnackBar(exception.message, "", 3000);
  }
}