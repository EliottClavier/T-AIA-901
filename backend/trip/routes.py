import json

from . import trip_bp

from flask import request

from path_finder import process_pathfinder, process_pathfinder_detailed
from nlp import process_nlp
from utils import split_request_data


@trip_bp.route('/', methods=['POST'])
def trip_route():
    sentences = split_request_data(request.data)
    results_nlp = process_nlp(sentences)

    sentences = results_nlp.split('\n')
    results_pathfinder = process_pathfinder(sentences)

    return results_pathfinder, 200, {'Content-Type': 'text/plain'}


@trip_bp.route('/details/', methods=['POST'])
def trip_details_route():
    data = json.loads(request.data)
    if 'sentence' not in data:
        return "Invalid request", 400, {'Content-Type': 'text/plain'}

    sentence_list = [f"1,{data['sentence']}"]
    results_nlp = process_nlp(sentence_list)

    sentence = results_nlp.split('\n')[0]
    results_pathfinder = process_pathfinder_detailed(sentence)

    code = 400
    if results_pathfinder["state"] == "CORRECT":
        code = 200
    return results_pathfinder, code, {'Content-Type': 'text/plain'}

