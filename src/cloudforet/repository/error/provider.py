from spaceone.core.error import *


class ERROR_NOT_EXIST_REQUIRED_FIELD(ERROR_INVALID_ARGUMENT):
    _message = '"{field}" field is required.'


class ERROR_INVALID_SOURCE_TYPE(ERROR_INVALID_ARGUMENT):
    _message = 'source_type must be GITHUB, but got "{source_type})"'


class ERROR_INSUFFICIENT_SYNC_OPTIONS(ERROR_INVALID_ARGUMENT):
    _message = 'MANUAL or AUTOMATIC sync_options require both source_type and source. ({sync_options})'


class ERROR_UNSUPPORT_SYNC_MODE(ERROR_INVALID_ARGUMENT):
    _message = 'The sync api does not support the "{sync_mode}" type of sync_mode. '


class ERROR_GITHUB_API(ERROR_INVALID_ARGUMENT):
    _message = '{error}'


class ERROR_INVALID_DATA_SCHEMA(ERROR_INVALID_ARGUMENT):
    _message = '{error}'
