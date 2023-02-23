import logging

from schema import Schema, Or, Optional
from spaceone.core.service import *
from cloudforet.repository.manager.provider_manager import ProviderManager
from cloudforet.repository.manager.github_manager import GithubManager
from cloudforet.repository.error.provider import *

_LOGGER = logging.getLogger(__name__)


class ProviderService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_mgr: ProviderManager = self.locator.get_manager(ProviderManager)
        self.github_mgr: GithubManager = self.locator.get_manager(GithubManager)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'name', 'domain_id'])
    def create(self, params):
        self._validate_data(params)

        params, secret_data = self._validate_sync_options(params)

        # This is code for phase 3
        if secret_data and params['sync_mode'] == 'AUTOMATIC':
            self._create_webhook_into_github(params, secret_data)

        return self.provider_mgr.create_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def update(self, params):
        self._validate_data(params)

        params, secret_data = self._validate_sync_options(params)
        provider_vo = self.provider_mgr.get_provider(params['provider'], params['domain_id'])

        # This is code for phase 3
        if secret_data and params['sync_mode'] == 'AUTOMATIC' and provider_vo.sync_mode != 'AUTOMATIC':
            self._create_webhook_into_github(params, secret_data)

        return self.provider_mgr.update_provider_by_vo(params, provider_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def sync(self, params):
        # This is code for phase 2
        provider_vo = self.get(params)
        self._check_sync_mode(provider_vo.sync_mode)

        repo_name = provider_vo.sync_options.source['url'].replace('https://github.com/', '')
        path = provider_vo.sync_options.source['path']
        provider_dict = self.github_mgr.get_provider(repo_name, path)
        self._check_sync_mode(provider_dict['sync_mode'])

        provider_dict, _ = self._validate_sync_options(provider_dict)

        return self.provider_mgr.update_provider_by_vo(provider_dict, provider_vo)

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

    def _create_webhook_into_github(self, params, secret_data):
        config = {
            'webhook_url': 'https://cloudforet.io', # This is temporary webhook url.
            'token': secret_data['token'],
            'repo_name': params['sync_options']['source']['url'].replace('https://github.com/', '')

        }
        self.github_mgr.create_webhook(config)

    @staticmethod
    def _validate_sync_options(params):
        secret_data = {}

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

                if params['sync_options']['source'].get('secret_data'):
                    secret_data = params['sync_options']['source'].pop('secret_data')

        return params, secret_data

    @staticmethod
    def _validate_data(params):
        schema_list = {
            'schema': Schema([
                {
                    'resource_type': Or('identity.ServiceAccount', 'secret.TrustedSecret', 'secret.Secret'),
                    Optional('secret_type'): Or('GENERAL', 'TRUSTED'),
                    'schema_id': Or('aws_service_account', 'aws_access_key', 'aws_assume_role')
                }
            ]),
            'description': Schema([
                {
                    'resource_type': 'identity.ServiceAccount',
                    'body': dict
                }
            ]),
            'reference': Schema([
                {
                    'resource_type': 'identity.ServiceAccount',
                    'link': dict
                }
            ])
        }

        for key in schema_list.keys():
            if params.get(key):
                schema = schema_list[key]
                data = params[key]
                try:
                    schema.validate(data)
                except Exception as e:
                    raise ERROR_INVALID_DATA_SCHEMA(error=e)

    @staticmethod
    def _check_sync_mode(sync_mode):
        if sync_mode not in ['MANUAL', 'AUTOMATIC']:
            raise ERROR_UNSUPPORT_SYNC_MODE(sync_mode=sync_mode)
