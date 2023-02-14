import logging
import sys

from spaceone.core.manager import BaseManager

from cloudforet.repository.error import *
from cloudforet.repository.model.remote_repository_model import RemoteRepository
from cloudforet.repository.connector.remote_repository_connector import RemoteRepositoryConnector

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_repository_connector: RemoteRepositoryConnector = \
            self.locator.get_connector(RemoteRepositoryConnector)

    def get_remote_repository(self, name):
        remote_repository_dict = self.remote_repository_connector.get_remote_repository(name)

        if remote_repository_dict:
            return remote_repository_dict

        raise ERROR_NO_REMOTE_REPOSITORY(name=name)

    def list_remote_repositories(self, name=None, version=None):
        remote_repository_list_of_dict = self.remote_repository_connector.list_remote_repositories(name=name,
                                                                                                   version=version)
        return remote_repository_list_of_dict

