import logging

from flask import Flask
from nlp import nlp_bp
from path_finder import pathfinder_bp
from trip import trip_bp

app = Flask(__name__)

app.register_blueprint(nlp_bp, url_prefix='/nlp')
app.register_blueprint(pathfinder_bp, url_prefix='/pathfinder')
app.register_blueprint(trip_bp, url_prefix='/trip')

logging.info("URL Map:", app.url_map)
logging.info("Configuration:", app.config)
logging.info("Blueprints:", app.blueprints)

if __name__ == '__main__':
    app.run(debug=True)

