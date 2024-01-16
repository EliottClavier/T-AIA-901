import re


def split_request_data(request_data):
    results = []
    for sentence in request_data.decode("utf-8").splitlines():
        if sentence.strip():
            expr = re.compile(r'(\d+),(.*)')
            match = expr.match(sentence)
            results.append(f"0,{sentence}" if not match else sentence)
    return results
