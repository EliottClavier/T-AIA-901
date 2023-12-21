from .path_finder import PathFinder

from flask import Blueprint

# Initialisation du Blueprint
pathfinder_bp = Blueprint('pathfinder', __name__)

# Import des routes
from . import routes
