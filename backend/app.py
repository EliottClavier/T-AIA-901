from flask import Flask
from nlp import nlp_bp
from path_finder import pathfinder_bp

app = Flask(__name__)

app.register_blueprint(nlp_bp, url_prefix='/nlp')
app.register_blueprint(pathfinder_bp, url_prefix='/pathfinder')

# Afficher les informations
print("URL Map:", app.url_map)
print("Configuration:", app.config)
print("Blueprints:", app.blueprints)

if __name__ == '__main__':
    app.run(debug=True)

