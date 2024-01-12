from . import pathfinder_bp

from flask import request

from .process_pathfinder import process_pathfinder
from nlp import process_nlp
from utils import split_request_data


@pathfinder_bp.route('/', methods=['POST'])
def pathfinder_route():
    sentences = split_request_data(request.data)
    results_nlp = process_nlp(sentences)

    sentences = results_nlp.split('\n')
    results_pathfinder = process_pathfinder(sentences)

    return results_pathfinder, 200, {'Content-Type': 'text/plain'}


@pathfinder_bp.route('/partial/', methods=['POST'])
def pathfinder_partial_route():
    sentences = split_request_data(request.data)
    results_pathfinder = process_pathfinder(sentences)

    return results_pathfinder, 200, {'Content-Type': 'text/plain'}
