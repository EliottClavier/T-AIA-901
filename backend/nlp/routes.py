from flask import jsonify, request
from . import nlp_bp  # Import du Blueprint initialisé dans __init__.py
from .nlp_functions import some_nlp_function

@nlp_bp.route('/', methods=['POST'])
def nlp_route():
    print("NLP route with input : ", request.json)
    result = {
       "sentenceID": "12345",
       "departure": "Paris",
       "destination": "Nantes",
       "steps": ["Lyon", "Avignon"]
   }
    return jsonify(result)
