import logging

from spaceone.core.service import *
from cloudforet.repository.manager.remote_repository_manager import RemoteRepositoryManager

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_repository_mgr: RemoteRepositoryManager = self.locator.get_manager(RemoteRepositoryManager)

    @transaction(append_meta={'authorization.scope': 'PUBLIC'})
    @check_required(['name'])
    def get(self, params):
        return self.remote_repository_mgr.get_remote_repository(params['name'])

    @transaction(append_meta={'authorization.scope': 'PUBLIC'})
    @append_keyword_filter(['name'])
    def list(self, params):
        return self.remote_repository_mgr.list_remote_repositories(params.get('name'), params.get('version'))
