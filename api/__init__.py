from flask import Flask
from api.controllers import data_bp, model_bp, dashboard_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(model_bp, url_prefix='/api/model')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    return app
