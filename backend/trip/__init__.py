from flask import Blueprint

# Initialisation du Blueprint
trip_bp = Blueprint('trip', __name__)

# Import des routes
from . import routes
