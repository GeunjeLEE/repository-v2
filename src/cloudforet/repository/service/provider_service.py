import logging

from spaceone.core.service import *
from cloudforet.repository.manager.provider_manager import ProviderManager
from cloudforet.repository.error.provider import *

_LOGGER = logging.getLogger(__name__)


class ProviderService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_mgr: ProviderManager = self.locator.get_manager(ProviderManager)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'name', 'domain_id'])
    def create(self, params):
        params = self._validate_sync_options(params)

        # TODO: Check using identity, secret api / long term
        #  'identity.ServiceAccount': 'aws_service_account',
        #  'secret.TrustedSecret': 'aws_access_key',
        #  'secret.Secret': ['aws_assume_role', 'aws_access_key']
        #  if params.get('schema'):
        #      call manager -> connector -> secret / identity

        # TODO: How do i validate description?
        #  if params.get('description'):
        #      pass

        return self.provider_mgr.create_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def update(self, params):
        provider_vo = self.provider_mgr.get_provider(params['provider'], params['domain_id'])
        return self.provider_mgr.update_provider_by_vo(params, provider_vo)

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

    @staticmethod
    def _validate_sync_options(params):
        if not params.get('sync_mode') or params['sync_mode'] == 'NONE':
            params['sync_options'] = {}
        else:
            if not params.get('sync_options'):
                raise ERROR_INSUFFICIENT_SYNC_OPTIONS(sync_options=params['sync_options'])
            else:
                if not params['sync_options'].get('source_type') or not params['sync_options'].get('source'):
                    raise ERROR_INSUFFICIENT_SYNC_OPTIONS(sync_options=params['sync_options'])

                if params['sync_options']['source_type'] != 'GITHUB':
                    raise ERROR_INVALID_SOURCE_TYPE(source_type=params['sync_options']['source_type'])

        return params
