from flask import Flask
from api.data_routes import data_bp
from api.model_routes import model_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(model_bp, url_prefix='/api/model')
    return app
