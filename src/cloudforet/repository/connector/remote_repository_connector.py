import logging

from spaceone.core.connector import BaseConnector
from spaceone.core import config

__all__ = ["RemoteRepositoryConnector"]

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryConnector(BaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remote_repositories = config.get_global("REMOTE_REPOSITORIES", [])

    def get_remote_repository(self, name):
        if self.remote_repositories:
            for repository in self.remote_repositories:
                if name == repository['name']:
                    return repository

        return {}

    def list_remote_repositories(self, name, version):
        if self.remote_repositories:
            if name or version:
                self._filter(name, version)

            return self.remote_repositories, len(self.remote_repositories)

        return [], 0

    def _filter(self, name, version):
        if name:
            self._pop('name', name)

        if version:
            self._pop('version', version)

    def _pop(self, key, value):
        for index, remote_repository in enumerate(self.remote_repositories):
            if value != remote_repository[key]:
                del self.remote_repositories[index]
