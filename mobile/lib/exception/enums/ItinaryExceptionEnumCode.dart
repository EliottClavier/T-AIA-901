enum ItineraryExceptionEnumCode {
  NOT_FRENCH("NOT_FRENCH", "Sorry, our model can't interpret languages other than French."),
  NOT_TRIP("NOT_TRIP", "Your request does not seem to correspond to an itinerary request"),
  UNKNOWN("UNKONWN", "An unknown error has occurred");

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