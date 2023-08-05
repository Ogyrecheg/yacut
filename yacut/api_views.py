from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import make_short_link


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    if not URLMap.check_short_link_in_db(short_id):
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    link = URLMap.query.filter_by(short=short_id).first()
    return jsonify({'url': link.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id', None)
    if custom_id is None or custom_id == '':
        custom_id = make_short_link()
        data.update({'custom_id': custom_id})

    if URLMap.check_short_link_in_db(custom_id):
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    if not URLMap.check_incoming_custom_id_by_regex(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    link = URLMap.create_link_and_add_in_db(data)
    return jsonify(link.to_dict()), HTTPStatus.CREATED
