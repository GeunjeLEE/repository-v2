DATABASE_AUTO_CREATE_INDEX = True
DATABASES = {
    'default': {
        'db': 'repository_v2',
        'host': 'localhost',
        'port': 27017,
        'username': 'repository_v2',
        'password': ''
    }
}
REMOTE_REPOSITORIES = []

CONNECTORS = {
    'GitHubConnector': {
        'GITHUB_READ_TOKEN': ''
    }
}