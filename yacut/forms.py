from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from yacut.constants import CUSTOM_LINK_LENGTH, ORIGINAL_URL_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Неправильный ввол ссылки'),
                    Length(max=ORIGINAL_URL_LENGTH)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=CUSTOM_LINK_LENGTH),
                    Optional()]
    )
    submit = SubmitField('Создать')
