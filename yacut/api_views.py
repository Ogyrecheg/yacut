from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import make_short_link


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    if not URLMap.check_short_link_exists(short_id):
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    link = URLMap.get_link_by_short_id(short_id)
    return jsonify({'url': link.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if ('custom_id' not in data or
            data['custom_id'] == '' or data['custom_id'] is None):
        data.update({'custom_id': make_short_link()})

    if URLMap.check_short_link_exists(data['custom_id']):
        raise InvalidAPIUsage(f'''Имя "{data['custom_id']}" уже занято.''')

    if not URLMap.check_incoming_custom_id_by_regex(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    link = URLMap.create_link_and_add_in_db(data['url'], data['custom_id'])
    return jsonify(link.to_dict()), HTTPStatus.CREATED
