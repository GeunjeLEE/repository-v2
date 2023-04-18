import logging

from spaceone.core.service import *
from cloudforet.repository.manager.provider_manager import ProviderManager
from cloudforet.repository.manager.remote_repository_manager import RemoteRepositoryManager
from cloudforet.repository.manager.source_manager import SourceManager
from cloudforet.repository.error.sync import *
from cloudforet.repository.libs.sync_utils import validate_sync_mode, parse_source_url, validate_params_data_schema

_LOGGER = logging.getLogger(__name__)


class ProviderService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_mgr: ProviderManager = self.locator.get_manager(ProviderManager)
        self.remote_repository_mgr: RemoteRepositoryManager = self.locator.get_manager(RemoteRepositoryManager)
        self.source_mgr: SourceManager = self.locator.get_manager(SourceManager)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'name', 'domain_id'])
    def create(self, params: dict):
        params, secret_data = validate_params_data_schema(params)

        if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC']:
            source_type = list(params['sync_options'].keys())[0]
            repo_name, directory, file = parse_source_url(params['sync_options'][source_type]['url'])
            path = f'{directory}/{file}'
            provider_data = self.source_mgr.get_source(source_type, repo_name, path)
            validate_params_data_schema(provider_data)
            provider_data.update(params)
            params = provider_data

        # TODO: phase 3
        # if secret_data and params['sync_mode'] == 'AUTOMATIC':
        #     self._create_webhook(params, secret_data)

        return self.provider_mgr.create_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def update(self, params: dict):
        params, secret_data = validate_params_data_schema(params)
        provider_vo = self.provider_mgr.get_provider(params['provider'], params['domain_id'])

        # TODO: phase 3
        #      The code that prevent duplicate webhook creation.
        # if secret_data and params['sync_mode'] == 'AUTOMATIC' and provider_vo.sync_mode != 'AUTOMATIC':
        #     self._create_webhook(params, secret_data)

        return self.provider_mgr.update_provider_by_vo(params, provider_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def sync(self, params: dict):
        provider_vo = self.provider_mgr.get_provider(params['provider'], params['domain_id'])
        validate_sync_mode(provider_vo.sync_mode)

        source_type = list(provider_vo['sync_options'].keys())[0]
        repo_name, directory, file = parse_source_url(provider_vo['sync_options'][source_type]['url'])
        path = f'{directory}/{file}'
        provider_data = self.source_mgr.get_source(source_type, repo_name, path)

        provider_data, _ = validate_params_data_schema(provider_data)
        validate_sync_mode(provider_data['sync_mode'])

        return self.provider_mgr.update_provider_by_vo(provider_data, provider_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def get(self, params: dict):
        provider_vos = self.provider_mgr.filter_providers(provider=params['provider'], domain_id=params['domain_id'])
        if provider_vos.count() == 1:
            return provider_vos[0].to_dict()
        else:
            provider_data = self.remote_repository_mgr.get_resource_from_remote_repository(
                'Provider', domain_id=params['domain_id'],
                only=params.get('only'),
                provider=params['provider']
            )

            if provider_data:
                return provider_data

        raise ERROR_NOT_FOUND(key='provider', value=params['provider'])

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['provider', 'domain_id'])
    def delete(self, params: dict):
        return self.provider_mgr.delete_provider(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['domain_id'])
    @append_query_filter(['provider', 'name', 'sync_mode', 'remote_repository_name', 'domain_id'])
    @append_keyword_filter(['provider', 'name'])
    def list(self, params: dict):
        query = params.get('query', {})

        local_providers_vos, local_total_count = self.provider_mgr.list_providers(query)
        local_providers_data = []
        for local_provider_vo in local_providers_vos:
            local_providers_data.append(local_provider_vo.to_dict())

        remote_providers_data, remote_total_count = self.remote_repository_mgr.list_resources_from_remote_repository(
            'Provider', query)

        providers = local_providers_data + remote_providers_data
        total_count = local_total_count + remote_total_count

        return providers, total_count

    # TODO: phase 3
    def _create_webhook(self, params: dict, secret_data: dict):
        repo_name, _, _ = parse_source_url(params['sync_options']['source']['url'])
        config = {
            'webhook_url': 'https://cloudforet.io',
            'token': secret_data['token'],
            'repo_name': repo_name

        }
        self.source_mgr.create_webhook(config)

    @staticmethod
    def _validate_params_data_schema(params: dict):
        secret_data = {}

        if not params.get('sync_mode') or params['sync_mode'] == 'NONE':
            params['sync_options'] = {}
        else:
            if not params.get('sync_options'):
                raise ERROR_INSUFFICIENT_SYNC_OPTIONS(sync_options=params['sync_options'])

        if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC']:
            source_type = list(params['sync_options'].keys())[0]
            if params['sync_options'][source_type].get('token'):
                secret_data = params['sync_options'][source_type].pop('token')

        return params, secret_data
