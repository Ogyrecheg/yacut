import re
from datetime import datetime
from http import HTTPStatus

from flask import url_for

from . import db

from .constants import API_REGEX_MATCH
from .error_handlers import InvalidAPIUsage
from .utils import make_short_link


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(23), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    @staticmethod
    def get_link_by_short_id(short_id):
        if not URLMap.short_link_exists(short_id):
            raise InvalidAPIUsage(
                'Указанный id не найден',
                HTTPStatus.NOT_FOUND
            )
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def short_link_exists(custom_id):
        return bool(
            URLMap.query.filter_by(short=custom_id).first()
        )

    @staticmethod
    def create_link_and_add_in_db_new(data, form_data_exists=False):
        if not form_data_exists:
            if not data:
                raise InvalidAPIUsage('Отсутствует тело запроса')

            if 'url' not in data:
                raise InvalidAPIUsage('"url" является обязательным полем!')

            URLMap.custom_id_exists_or_create(data)

            if URLMap.short_link_exists(data['custom_id']):
                raise InvalidAPIUsage(
                    f'''Имя "{data['custom_id']}" уже занято.'''
                )

            if not URLMap.check_incoming_custom_id_by_regex(data['custom_id']):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )
            original_url = data['url']
        else:
            URLMap.custom_id_exists_or_create(data)
            original_url = data['original_link']

        link = URLMap(original=original_url, short=data['custom_id'])
        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def check_incoming_custom_id_by_regex(custom_id):
        return bool(
            re.match(API_REGEX_MATCH, custom_id)
        )

    @staticmethod
    def custom_id_exists_or_create(data):
        if ('custom_id' not in data or
                data['custom_id'] == '' or data['custom_id'] is None):
            data.update({'custom_id': make_short_link()})
        return data
