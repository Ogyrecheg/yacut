import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .constants import API_REGEX_MATCH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is not None:
        return jsonify({'url': link.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id', None)
    if custom_id is None or custom_id == '':
        data['custom_id'] = get_unique_short_id()

    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    if not re.match(API_REGEX_MATCH, data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED
