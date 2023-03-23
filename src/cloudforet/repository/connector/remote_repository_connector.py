import copy
import logging

from google.protobuf.json_format import MessageToDict
from spaceone.core.connector import BaseConnector
from spaceone.core import config
from spaceone.core import pygrpc, utils

__all__ = ["RemoteRepositoryConnector"]

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryConnector(BaseConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remote_repositories = config.get_global("REMOTE_REPOSITORIES", [])
        self.grpc_clients_info = self._get_remote_repository_endpoints()

    def get_provider_from_remote_repositories(self, provider, domain_id, only):
        params = {
            'domain_id': domain_id,
            'provider': provider,
            'only': only
        }

        if self.grpc_clients_info:
            for grpc_client_info in self.grpc_clients_info:
                try:
                    provider_vo = grpc_client_info['grpc_client'].Provider.get(params)
                    provider_data = MessageToDict(provider_vo, preserving_proto_field_name=True)

                    provider_data['remote_repository'] = grpc_client_info['remote_repository']
                    provider_data['domain_id'] = domain_id

                    return provider_data
                except Exception:
                    pass

        return False

    def list_provider_from_remote_repositories(self, query: dict):
        """
        :return: results: list, total_count: int
        """
        providers_info_from_remote_repositories = []
        total_count_from_remote_repositories = 0

        domain_id = self._get_domain_id_from_query(query)
        params = {
            'query': query,
            'domain_id': domain_id
        }

        if self.grpc_clients_info:
            for grpc_client_info in self.grpc_clients_info:
                providers_message = grpc_client_info['grpc_client'].Provider.list(params)
                providers_data = MessageToDict(providers_message, preserving_proto_field_name=True)

                if not providers_data.get('results'):
                    continue

                for provider in providers_data['results']:
                    provider['remote_repository'] = grpc_client_info['remote_repository']
                    provider['domain_id'] = domain_id

                providers_info_from_remote_repositories += providers_data['results']
                total_count_from_remote_repositories += providers_data['total_count']

        return providers_info_from_remote_repositories, total_count_from_remote_repositories

    def get_remote_repository(self, name: str):
        for repository in self.remote_repositories:
            if name == repository.get('name'):
                return repository

        return {}

    def list_remote_repositories(self, name: str, version: str):
        remote_repositories = self.remote_repositories

        if name or version:
            remote_repositories = self._filter(name, version)

        return remote_repositories, len(remote_repositories)

    def _filter(self, name: str, version: str):
        _remote_repositories = copy.deepcopy(self.remote_repositories)

        if name:
            self._pop('name', name, _remote_repositories)

        if version:
            self._pop('version', version, _remote_repositories)

        return _remote_repositories

    def _get_remote_repository_endpoints(self):
        grpc_clients = []
        if self.remote_repositories:
            for remote_repository in self.remote_repositories:
                e = utils.parse_grpc_endpoint(remote_repository['endpoint'])
                grpc_client = pygrpc.client(endpoint=e['endpoint'], ssl_enabled=e['ssl_enabled'])

                grpc_clients.append({
                    'remote_repository': remote_repository,
                    'grpc_client': grpc_client
                })

        return grpc_clients

    @staticmethod
    def _pop(key: str, value: str, remote_repositories: list):
        for index, remote_repository in enumerate(remote_repositories):
            if value != remote_repository[key]:
                del remote_repositories[index]

    @staticmethod
    def _get_domain_id_from_query(raw_query):
        query = copy.deepcopy(raw_query)

        for filters in query['filter']:
            key = filters['k']
            if key == 'domain_id':
                return filters['v']
