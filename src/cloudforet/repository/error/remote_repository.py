from spaceone.core.error import *


class ERROR_NO_REMOTE_REPOSITORY(ERROR_INVALID_ARGUMENT):
    _message = 'Remote Repository not found. (name = {name})'
