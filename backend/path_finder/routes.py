import os

from flask import jsonify
from . import pathfinder_bp  # Import du Blueprint initialisé dans __init__.py
from .path_finder import PathFinder


@pathfinder_bp.route('/')
def pathfinder_route():

    trip_order = ["Nantes", "Lyon"]

    result = PathFinder.get_shortest_path(trip_order)

    return jsonify({"result": result})
