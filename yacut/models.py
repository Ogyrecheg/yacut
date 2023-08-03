from datetime import datetime

from flask import url_for

from . import db
from .constants import API_FIELDS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(23), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for('index_view', _external=True) + self.short
        )

    def from_dict(self, data):
        for field in API_FIELDS.keys():
            if field in data:
                setattr(self, API_FIELDS[field], data[field])
