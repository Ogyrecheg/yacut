import random
import re

from . import db
from .constants import API_REGEX_MATCH, MAX_LENGTH_SHORT_ID, SYMBOLS
from .exceptions import (DataNotExists, FailedVerificationByRegex,
                         ShortLinkExists, ShortURLNotFound, URLNotExistsInData)
from .models import URLMap


class URLMapCreator:
    @staticmethod
    def make_short_link():
        return ''.join(random.sample(SYMBOLS, MAX_LENGTH_SHORT_ID))

    @staticmethod
    def get_link_by_short_id(short_id):
        if not URLMap.query.filter_by(short=short_id).first():
            raise ShortURLNotFound

    @staticmethod
    def short_link_exists(custom_id):
        if URLMap.query.filter_by(short=custom_id).first():
            raise ShortLinkExists

    @staticmethod
    def create_link_and_add_in_db_new(data, form_data_exists=False):
        if not form_data_exists:
            if not data:
                raise DataNotExists
            if 'url' not in data:
                raise URLNotExistsInData
            URLMapCreator.custom_id_exists_or_create(data)
            URLMapCreator.short_link_exists(data['custom_id'])
            if not URLMapCreator.check_incoming_custom_id_by_regex(data['custom_id']):
                raise FailedVerificationByRegex
            original_url = data['url']
        else:
            URLMapCreator.custom_id_exists_or_create(data)
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
            data.update({'custom_id': URLMapCreator.make_short_link()})
        return data
