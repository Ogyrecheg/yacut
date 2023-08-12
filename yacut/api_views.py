from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .exceptions import (DataNotExists, FailedVerificationByRegex,
                         ShortLinkExists, ShortURLNotFound, URLNotExistsInData)
from .services import URLMapCreator


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    try:
        return jsonify(
            {'url': URLMapCreator.get_link_by_short_id(short_id).original}
        ), HTTPStatus.OK
    except ShortURLNotFound:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND
        )


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    data = request.get_json(silent=True)
    try:
        return jsonify(
            URLMapCreator.create_link_and_add_in_db_new(data).to_dict()
        ), HTTPStatus.CREATED
    except DataNotExists:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    except URLNotExistsInData:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    except ShortLinkExists:
        raise InvalidAPIUsage(
            f'''Имя "{data['custom_id']}" уже занято.'''
        )
    except FailedVerificationByRegex:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки'
        )
