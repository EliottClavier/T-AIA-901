def split_request_data(request_data):
    return [sentence for sentence in request_data.decode("utf-8").splitlines() if sentence.strip()]