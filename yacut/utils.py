import random

from .constants import MAX_LENGTH_SHORT_ID, SYMBOLS


def make_short_link():
    """Функция генерации короткой ссылки."""
    return ''.join(random.sample(SYMBOLS, MAX_LENGTH_SHORT_ID))
