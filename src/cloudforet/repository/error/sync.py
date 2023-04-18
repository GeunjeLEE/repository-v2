from spaceone.core.error import *


class ERROR_INSUFFICIENT_SYNC_OPTIONS(ERROR_INVALID_ARGUMENT):
    _message = 'MANUAL or AUTOMATIC sync_options require source information. ({sync_options})'


class ERROR_UNSUPPORT_SYNC_MODE(ERROR_INVALID_ARGUMENT):
    _message = 'The sync api does not support the "{sync_mode}" type of sync_mode. '
