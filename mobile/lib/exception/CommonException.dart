
class CommonException implements Exception {
  late String code;
  late String message;

  CommonException(String code, String message) {
    this.code = code;
    this.message = message;
  }

}