import logging

from spaceone.core.manager import BaseManager
from cloudforet.repository.model.remote_repository_model import RemoteRepository

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_repository_model: RemoteRepository = self.locator.get_model(RemoteRepository)

    def get_remote_repository(self, name): # name argument passed by service
        return self.remote_repository_model.get(name=name)

    def list_remote_repository(self, query):
        return self.remote_repository_model.query(**query)
