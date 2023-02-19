from spaceone.core.error import *


class ERROR_NO_REMOTE_REPOSITORY(ERROR_INVALID_ARGUMENT):
    _message = 'Remote Repository not found. (name = {name})'


class ERROR_INVALID_SOURCE_TYPE(ERROR_INVALID_ARGUMENT):
    _message = 'source_type must be GITHUB, but got "{source_type})"'


class ERROR_INSUFFICIENT_SYNC_OPTIONS(ERROR_INVALID_ARGUMENT):
    _message = 'MANUAL or AUTOMATIC sync_options require both source_type and source. ({sync_options})'
