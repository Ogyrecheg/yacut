import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import API_REGEX_MATCH


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
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def check_short_link_exists(custom_id):
        return bool(
            URLMap.query.filter_by(short=custom_id).first()
        )

    @staticmethod
    def create_link_and_add_in_db(original_link, custom_id):
        link = URLMap(original=original_link, short=custom_id)
        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def check_incoming_custom_id_by_regex(custom_id):
        return bool(
            re.match(API_REGEX_MATCH, custom_id)
        )
