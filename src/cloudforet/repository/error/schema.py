from spaceone.core.error import *


class ERROR_INVALID_SCHEMA(ERROR_INVALID_ARGUMENT):
    _message = 'Schema format(JSON SCHEMA) is invalid. (schema = {schema})'