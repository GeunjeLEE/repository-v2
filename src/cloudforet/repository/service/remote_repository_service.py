import logging

from spaceone.core.service import *
from cloudforet.repository.manager.remote_repository_manager import RemoteRepositoryManager

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.remote_repository_mgr: RemoteRepositoryManager = self.locator.get_manager(RemoteRepositoryManager)

    @transaction(append_meta={'authorization.scope': 'PUBLIC'})
    @check_required(['name'])
    def get(self, params):
        return self.remote_repository_mgr.get_remote_repository(params['name'])

    @transaction(append_meta={'authorization.scope': 'PUBLIC'})
    @append_query_filter(['name', 'version'])
    @append_keyword_filter(['name'])
    def list(self, params):
        query = params.get('query', {})

        return self.remote_repository_mgr.list_remote_repository(query)
