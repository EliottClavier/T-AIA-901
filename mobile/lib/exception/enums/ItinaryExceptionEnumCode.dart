enum ItineraryExceptionEnumCode {
  NOT_FRENCH("NOT_FRENCH", "Les autres langues que le français ne sont pas prises en charge."),
  NOT_TRIP("NOT_TRIP", "La commande n'est pas une commande de voyage."),
  UNKNOWN("UNKNOWN", "La commande n'est pas valide ou une erreur inconnue est survenue.");

  const ItineraryExceptionEnumCode(this._code, this._message);
  final String _message;
  final String _code;

  getCode(){
    return this._code;
  }

  getMessage(){
    return this._message;
  }

  factory ItineraryExceptionEnumCode.fromCode(String code){
    for(var value in ItineraryExceptionEnumCode.values){
      if(value.getCode() == code){
        return value;
      }
    }
    return UNKNOWN;
  }
}