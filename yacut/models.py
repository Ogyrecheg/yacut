from datetime import datetime

from flask import url_for

from . import db
from .constants import CUSTOM_LINK_LENGTH, ORIGINAL_URL_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGTH), nullable=False)
    short = db.Column(db.String(CUSTOM_LINK_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )
