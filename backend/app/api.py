from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/data', methods=['GET'])
def get_data():
    return jsonify({'key': 'value'})