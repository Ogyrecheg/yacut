import random

from .constants import MAX_LENGTH_SHORT_ID, SYMBOLS


def get_unique_short_id():
    """Функция генерации уникального ID для короткой ссылки."""
    return ''.join(random.sample(SYMBOLS, MAX_LENGTH_SHORT_ID))
