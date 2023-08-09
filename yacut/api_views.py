from http import HTTPStatus

from flask import jsonify, request

from . import app
from .models import URLMap


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    return jsonify(
        {'url': URLMap.get_link_by_short_id(short_id).original}
    ), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    return jsonify(
        URLMap.create_link_and_add_in_db_new(data).to_dict()
    ), HTTPStatus.CREATED
