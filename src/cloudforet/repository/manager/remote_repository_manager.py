import logging
import copy

from spaceone.core.manager import BaseManager

from cloudforet.repository.error import *
from cloudforet.repository.connector.remote_repository_connector import RemoteRepositoryConnector

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_repository_connector: RemoteRepositoryConnector = \
            self.locator.get_connector(RemoteRepositoryConnector)

    def get_remote_repository(self, name: str):
        remote_repository_dict = self.remote_repository_connector.get_remote_repository(name)

        if remote_repository_dict:
            return remote_repository_dict

        raise ERROR_NOT_FOUND(key='name', value=name)

    def list_remote_repositories(self, name=None, version=None):
        return self.remote_repository_connector.list_remote_repositories(name=name, version=version)

    def get_provider(self, provider: str, domain_id: str, only=None):
        return self.remote_repository_connector.get_provider_from_remote_repositories(provider, domain_id, only)

    def list_providers(self, query: dict):
        """
        :return: results: list of dict, total_count: int
        """

        # remote_repository_name is not for the list api
        remote_repository_name_filter = {}
        filtered_query = copy.deepcopy(query)
        for index, filter_kv in enumerate(filtered_query['filter']):
            if filter_kv['k'] == 'remote_repository_name':
                remote_repository_name_filter = filtered_query['filter'].pop(index)

        providers_data, total_count = self.remote_repository_connector.list_provider_from_remote_repositories(filtered_query)

        if remote_repository_name_filter:
            providers_data, total_count = self._filter_by_remote_repository_filter(providers_data,
                                                                                   remote_repository_name_filter)

        return providers_data, total_count

    @staticmethod
    def _filter_by_remote_repository_filter(raw_providers_data, remote_repository_name_filter):
        providers_data = copy.deepcopy(raw_providers_data)
        for index, provider_data in enumerate(providers_data):
            if provider_data['remote_repository'].get('name') != remote_repository_name_filter['v']:
                del providers_data[index]

        return providers_data, len(providers_data)
