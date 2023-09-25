from flask import jsonify
from . import nlp_bp  # Import du Blueprint initialisé dans __init__.py
from .nlp_functions import some_nlp_function

@nlp_bp.route('/')
def nlp_route():
    print("NLP route")
    result = some_nlp_function()
    return jsonify({"result": result})
