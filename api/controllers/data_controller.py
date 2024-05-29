import json

from flask import Blueprint, jsonify

from api.services import BagOfWordsService, IndicatorsService, StatisticsService

data_bp = Blueprint('data', __name__)


@data_bp.route('/metadata', methods=['GET'])
def get_metadata_route():
    with open('metadata.json', 'r') as file:
        metadata = json.load(file)

    return jsonify(metadata)


@data_bp.route('/bag_of_words', methods=['GET'])
def get_bag_of_words():
    return jsonify(BagOfWordsService.get_words())


@data_bp.route('/indicators', methods=['GET'])
def get_indicators():
    return jsonify(IndicatorsService.get_indicators())


@data_bp.route('/charts/bar', methods=['GET'])
def get_bar_data():
    return jsonify(StatisticsService.get_bar_data())


@data_bp.route('/charts/pie', methods=['GET'])
def get_pie_data():
    return jsonify(StatisticsService.get_pie_data())


@data_bp.route('/charts/map', methods=['GET'])
def get_map_data():
    return jsonify(StatisticsService.get_map_data())


@data_bp.route('/charts/treemap', methods=['GET'])
def get_treemap_data():
    return jsonify(StatisticsService.get_treemap_data())
