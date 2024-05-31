from flask import Blueprint, jsonify, request

from api.services import TopicService

model_bp = Blueprint('model', __name__)


@model_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    return jsonify(TopicService.predict_topic(text))


@model_bp.route('/topics', methods=['GET'])
def get_all_topics():
    return jsonify(TopicService.get_topics())


@model_bp.route('/topics/<int:topic_id>', methods=['GET'])
def get_topic(topic_id):
    return jsonify(TopicService.get_topic(topic_id))


@model_bp.route('/intertopic', methods=['GET'])
def get_intertopic_data():
    return jsonify(TopicService.get_vizualization_data())
