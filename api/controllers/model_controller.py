from flask import Blueprint, jsonify, current_app

from api.services import TopicService

model_bp = Blueprint('model', __name__)


@model_bp.route('/predict', methods=['POST'])
def predict():
    if 'model' not in current_app:
        return jsonify({"error": "Modelo no cargado"}), 500

    # Aquí va la lógica de predicción usando current_app.model

    return jsonify({"message": "Predicción realizada exitosamente"})


@model_bp.route('/topics', method=['GET'])
def get_all_topics():
    return jsonify(TopicService.get_topics())
