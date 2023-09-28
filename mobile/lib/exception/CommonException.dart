
class CommonException implements Exception {
  late String message;
  late String code;

  CommonException(String message, String code) {
    this.message = message;
    this.code = code;
  }

}