import 'package:mobile/exception/CommonException.dart';
import 'package:mobile/exception/enums/ItinaryExceptionEnumCode.dart';

class ItinaryException extends CommonException {

  ItinaryException(super.message, super.code);

  factory ItinaryException.createFromEnumCode(ItinaryExceptionEnumCode code, String? sentenceId){
    String message = code.getMessage();
    if(sentenceId!.isNotEmpty){
      message = "Sentence Id : $sentenceId, Error message : " + message;
    }
    return ItinaryException(
        code.getCode(),
        message
    );
  }

  @override
  String toString() {
    return "ItinaryException : " + this.message;
  }
}