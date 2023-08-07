import string

CUSTOM_LINK_LENGTH = 16
ORIGINAL_URL_LENGTH = 2028
MAX_LENGTH_SHORT_ID = 6
SYMBOLS = string.ascii_letters + string.digits
API_REGEX_MATCH = r'^[a-zA-Z\d]{1,16}$'
FORM_REGEX_MATCH = r'^[a-zA-Z\d]{1,6}$'
