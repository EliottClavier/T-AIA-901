from . import nlp_bp  # Import du Blueprint initialisé dans __init__.py
from .process_classification import process_nlp, process_text_classification, process_token_classification
from utils import split_request_data

from flask import request

@nlp_bp.route('/', methods=['POST'])
def nlp_route():
    sentences = split_request_data(request.data)
    results = process_nlp(sentences)
    return results, 200, {'Content-Type': 'text/plain'}


@nlp_bp.route('/text/', methods=['POST'])
def text_classification_route():
    sentences = split_request_data(request.data)
    results = process_text_classification(sentences)
    return results, 200, {'Content-Type': 'text/plain'}


@nlp_bp.route('/token/', methods=['POST'])
def token_classification_route():
    sentences = split_request_data(request.data)
    sentences = [
        sentence
        for sentence in sentences
        if (parts := sentence.split(','))
           and len(parts) > 1
           and parts[1] not in ["NOT_TRIP", "NOT_FRENCH", "UNKNOWN"]
    ]
    results = process_token_classification(sentences)
    return results, 200, {'Content-Type': 'text/plain'}