from flask import jsonify
from . import pathfinder_bp  # Import du Blueprint initialisé dans __init__.py
from .pathfinder_functions import some_pathfinder_function


@pathfinder_bp.route('/')
def pathfinder_route():
    result = some_pathfinder_function()
    return jsonify({"result": result})
