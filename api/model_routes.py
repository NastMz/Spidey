from flask import Blueprint, jsonify, current_app
import joblib

model_bp = Blueprint('model', __name__)


@model_bp.before_request
def load_global_model():
    model_path = 'trained_model.joblib'  # Define la ruta del modelo
    current_app.model = joblib.load(model_path)


@model_bp.route('/predict', methods=['POST'])
def predict():
    if 'model' not in current_app:
        return jsonify({"error": "Modelo no cargado"}), 500

    # Aquí va la lógica de predicción usando current_app.model

    return jsonify({"message": "Predicción realizada exitosamente"})
