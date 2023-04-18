from spaceone.core.error import *


class ERROR_NOT_EXIST_REQUIRED_FIELD(ERROR_INVALID_ARGUMENT):
    _message = '"{field}" field is required.'

