from spaceone.core.error import *


class ERROR_GITHUB_OBJECT_NOT_FOUND(ERROR_NOT_FOUND):
    _message = "Github object not found (reason = {reason})"

class ERROR_RATE_LIMIT_EXCEEDED(ERROR_BASE):
    _message = 'API rate limit exceeded, you can increase the API limit by setting the GITHUB_READ_TOKEN in the connector configuration'
