from . import pathfinder_bp

from flask import request

from .process_pathfinder import process_pathfinder
from utils import split_request_data


@pathfinder_bp.route('/', methods=['POST'])
def pathfinder_partial_route():
    sentences = split_request_data(request.data)
    results_pathfinder = process_pathfinder(sentences)

    return results_pathfinder, 200, {'Content-Type': 'text/plain'}
