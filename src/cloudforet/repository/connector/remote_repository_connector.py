import copy
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
        for repository in self.remote_repositories:
            if name == repository.get('name'):
                return repository

        return {}

    def list_remote_repositories(self, name, version):
        remote_repositories = self.remote_repositories

        if name or version:
            remote_repositories = self._filter(name, version)

        return remote_repositories, len(remote_repositories)

    def _filter(self, name, version):
        _remote_repositories = copy.deepcopy(self.remote_repositories)

        if name:
            self._pop('name', name, _remote_repositories)

        if version:
            self._pop('version', version, _remote_repositories)

        return _remote_repositories

    @staticmethod
    def _pop(key, value, remote_repositories):
        for index, remote_repository in enumerate(remote_repositories):
            if value != remote_repository[key]:
                del remote_repositories[index]


