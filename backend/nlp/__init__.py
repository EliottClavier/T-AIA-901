from flask import Blueprint

# Initialisation du Blueprint
nlp_bp = Blueprint('nlp', __name__)

# Import des routes
from . import routes