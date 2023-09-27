enum ItinaryExceptionEnumCode {
  NOT_FRENCH("NOT_FRENCH", "Sorry, our model can't interpret languages other than French."),
  NOT_TRIP("NOT_TRIP", "Your request does not seem to correspond to an itinerary request"),
  UNKNOWN("UNKONWN", "An unknown error has occurred");

  const ItinaryExceptionEnumCode(this._code, this._message);
  final String _code;
  final String _message;

  getCode(){
    return this._code;
  }

  getMessage(){
    return this._message;
  }
}