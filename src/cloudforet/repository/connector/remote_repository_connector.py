import logging

from spaceone.core.connector import BaseConnector
from spaceone.core import config

__all__ = ["RemoteRepositoryConnector"]

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryConnector(BaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remote_repositories = config.get_global("REMOTE_REPOSITORIES", {})

    def get_remote_repository(self, name):
        if self.remote_repositories:
            for repository in self.remote_repositories:
                if name == repository['name']:
                    return repository

        return {}

    def list_remote_repositories(self, name, version):
        if self.remote_repositories:
            return self._list_remote_repositories_filter(self.remote_repositories, name, version)

        return [], 0

    @staticmethod
    def _list_remote_repositories_filter(remote_repositories, name, version):
        filtered_remote_repositories = []

        if name and version:
            for repository in remote_repositories:
                if name == repository['name'] and version == repository['version']:
                    filtered_remote_repositories.append(repository)
        elif name:
            for repository in remote_repositories:
                if name == repository['name']:
                    filtered_remote_repositories.append(repository)
        elif version:
            for repository in remote_repositories:
                if version == repository['version']:
                    filtered_remote_repositories.append(repository)
        else:
            filtered_remote_repositories = remote_repositories

        return filtered_remote_repositories, len(filtered_remote_repositories)

