import logging

from spaceone.core.manager import BaseManager
from cloudforet.repository.model.provider_model import Provider

_LOGGER = logging.getLogger(__name__)


class ProviderManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provider_model: Provider = self.locator.get_model(Provider)

    def create_provider(self, params):
        def _rollback(provider_vo: Provider):
            _LOGGER.info(f'[ROLLBACK] Delete provider : {provider_vo.provider}')
            provider_vo.delete()

        provider_vo: Provider = self.provider_model.create(params)
        self.transaction.add_rollback(_rollback, provider_vo)

        return provider_vo

    def update_provider(self, params):
        provider_vo: Provider = self.get_provider(params['provider'], params['domain_id'])

        return self.update_provider_by_vo(params, provider_vo)

    def update_provider_by_vo(self, params: dict, provider_vo: Provider):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Update provider: {provider_vo.provider}')
            provider_vo.update(old_data)

        self.transaction.add_rollback(_rollback, provider_vo.to_dict())

        return provider_vo.update(params)

    def sync_provider(self, params):
        pass

    def delete_provider(self, params):
        provider_vo: Provider = self.get_provider(params['provider'], params['domain_id'])
        provider_vo.delete()

    def get_provider(self, provider, domain_id, only=None):
        return self.provider_model.get(provider=provider, domain_id=domain_id, only=only)

    def list_providers(self, query):
        return self.provider_model.query(**query)
