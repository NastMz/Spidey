from flask import Blueprint, request, jsonify
from data_analysis.processing_pipeline import (
    get_metadata
)

data_bp = Blueprint('data', __name__)


@data_bp.route('/metadata', methods=['GET'])
def get_metadata_route():
    metadata = get_metadata()
    return jsonify(metadata)
