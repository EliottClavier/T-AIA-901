import 'package:mobile/exception/CommonException.dart';
import 'enums/ItinaryExceptionEnumCode.dart';

class ItineraryException extends CommonException {

  ItineraryException(super.code, super.message);

  factory ItineraryException.createFromEnumCode(ItineraryExceptionEnumCode code){
    String message = code.getCode() + ": " + code.getMessage();
    return ItineraryException(
        code.getCode(),
        message
    );
  }

  @override
  String toString() {
    return "ItineraryException : " + this.message;
  }
}