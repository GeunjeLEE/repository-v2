import logging

from spaceone.core.service import *
from cloudforet.repository.manager.provider_manager import ProviderManager

_LOGGER = logging.getLogger(__name__)


class ProviderService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.provider_mgr: ProviderManager = self.locator.get_manager(ProviderManager)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'name', 'domain_id'])
    def create(self, params):
        """ TODO: Add description
        Args:
            params (dict): {

            }

        Returns:
            provider_vo (object)
        """
        return self.provider_mgr.create_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def update(self, params):
        return self.provider_mgr.update_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def sync(self, params):
        return self.provider_mgr.sync_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def get(self, params):
        return self.provider_mgr.get_provider(params['provider'], params['domain_id'], params.get('only'))

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def delete(self, params):
        return self.provider_mgr.delete_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['domain_id'])
    @append_query_filter(['provider', 'name', 'sync_mode', 'domain_id'])
    @append_keyword_filter(['provider', 'name'])
    def list(self, params):
        query = params.get('query', {})

        return self.provider_mgr.list_providers(query)
