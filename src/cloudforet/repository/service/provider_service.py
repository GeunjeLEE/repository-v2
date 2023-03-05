import logging

from schema import Schema, Or, Optional, Regex
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
    def create(self, params: dict):
        params, secret_data = self._validate_data(params)

        # Verifying that the github repository and files actually exist before creating the provider resource.
        if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC']:
            repo_name, directory, file = self._parse_source_url(params['sync_options']['source']['url'])
            path = f'{directory}/{file}'
            provider_dict = self.github_mgr.get_provider(repo_name, path)
            self._validate_data(provider_dict)

            params = dict(list(provider_dict.items()) + list(params.items()))

        # TODO: phase 3
        # if secret_data and params['sync_mode'] == 'AUTOMATIC':
        #     self._create_webhook_into_github(params, secret_data)

        return self.provider_mgr.create_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def update(self, params: dict):
        params, secret_data = self._validate_data(params)
        provider_vo = self.provider_mgr.get_provider(params['provider'], params['domain_id'])

        # TODO: phase 3
        #      The code that prevent duplicate webhook creation.
        # if secret_data and params['sync_mode'] == 'AUTOMATIC' and provider_vo.sync_mode != 'AUTOMATIC':
        #     self._create_webhook_into_github(params, secret_data)

        return self.provider_mgr.update_provider_by_vo(params, provider_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def sync(self, params: dict):
        provider_vo = self.get(params)
        self._validate_sync_mode(provider_vo.sync_mode)

        repo_name, directory, file = self._parse_source_url(provider_vo['sync_options']['source']['url'])
        path = f'{directory}/{file}'
        provider_dict = self.github_mgr.get_provider(repo_name, path)

        provider_dict, _ = self._validate_data(provider_dict)
        self._validate_sync_mode(provider_dict['sync_mode'])

        return self.provider_mgr.update_provider_by_vo(provider_dict, provider_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def get(self, params: dict):
        return self.provider_mgr.get_provider(params['provider'], params['domain_id'], params.get('only'))

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def delete(self, params: dict):
        return self.provider_mgr.delete_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['domain_id'])
    @append_query_filter(['provider', 'name', 'sync_mode', 'domain_id'])
    @append_keyword_filter(['provider', 'name'])
    def list(self, params: dict):
        query = params.get('query', {})

        return self.provider_mgr.list_providers(query)

    # TODO: phase 3
    def _create_webhook_into_github(self, params: dict, secret_data: dict):
        repo_name, _, _ = self._parse_source_url(params['sync_options']['source']['url'])
        config = {
            'webhook_url': 'https://cloudforet.io',
            'token': secret_data['token'],
            'repo_name': repo_name

        }
        self.github_mgr.create_webhook(config)

    @staticmethod
    def _validate_data(params: dict):
        secret_data = {}

        if not params.get('sync_mode') or params['sync_mode'] == 'NONE':
            params['sync_options'] = {}
        else:
            if not params.get('sync_options'):
                raise ERROR_INSUFFICIENT_SYNC_OPTIONS(sync_options=params['sync_options'])

        schema_list = {
            'sync_mode': Schema(Or('NONE', 'MANUAL', 'AUTOMATIC')),
            'sync_options': Schema(
                {
                    'source_type': 'GITHUB',
                    'source': {
                        'url': Regex(
                            r'[-a-zA-Z0-9@:%._\+~#=]*\/[-a-zA-Z0-9@:%._\+~#=]*\/[-a-zA-Z0-9@:%._\+~#=]*\/[a-z]*\.yaml',
                            error='Invalid url format, url must be "org/repo_name/directory/provider.yaml"'
                        ),
                        Optional('secret_data'): {
                            'token': str
                        },
                    },
                }
            ),
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

        if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC'] and params['sync_options']['source'].get('secret_data'):
            secret_data = params['sync_options']['source'].pop('secret_data')

        return params, secret_data

    @staticmethod
    def _validate_sync_mode(sync_mode: str):
        if sync_mode not in ['MANUAL', 'AUTOMATIC']:
            raise ERROR_UNSUPPORT_SYNC_MODE(sync_mode=sync_mode)

    @staticmethod
    def _parse_source_url(url):
        repo_name = f'{url.split("/")[0]}/{url.split("/")[1]}'
        directory = url.split("/")[2]
        file = url.split("/")[3]
        return repo_name, directory, file
