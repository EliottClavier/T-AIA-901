import 'package:mobile/exception/CommonException.dart';
import 'enums/ItinaryExceptionEnumCode.dart';

class ItineraryException extends CommonException {

  ItineraryException(super.code, super.message);

  factory ItineraryException.createFromEnumCode(ItineraryExceptionEnumCode code, String? sentenceId){
    String message = code.getMessage();
    if(sentenceId!.isNotEmpty){
      message = "Sentence Id : $sentenceId, Error message : " + message;
    }
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