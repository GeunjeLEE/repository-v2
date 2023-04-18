import logging
import copy
import functools

from spaceone.core.manager import BaseManager

from google.protobuf.json_format import MessageToDict
from spaceone.core import config
from spaceone.core.connector.space_connector import SpaceConnector
from cloudforet.repository.error import *

_LOGGER = logging.getLogger(__name__)


class RemoteRepositoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_repositories = config.get_global("REMOTE_REPOSITORIES", [])

    def get_remote_repository(self, name: str):
        for repository in self.remote_repositories:
            if name == repository['name']:
                return repository

        raise ERROR_NOT_FOUND(key='name', value=name)

    def list_remote_repositories(self, name=None, version=None):
        remote_repositories = self.remote_repositories

        if name or version:
            remote_repositories = []
            for repository in filter(functools.partial(self._remote_repository_filter, name, version),
                                     self.remote_repositories):
                remote_repositories.append(repository)

        return remote_repositories, len(remote_repositories)

    def list_resources_from_remote_repository(self, resource: str, query: dict):
        conns_by_remote_repository = self._create_conns_by_remote_repository()
        method = f'{resource}.list'

        query, remote_repository_name = self._pop_remote_repository_name_from_query(query)
        query, local_domain_id = self._pop_local_domain_id_from_query(query)

        resources_data_from_remote = []
        total_count_from_remote = 0
        if conns_by_remote_repository:
            for conn_with_remote_repository in conns_by_remote_repository:
                remote_domain_id = conn_with_remote_repository['remote_repository']['domain_id']
                if remote_domain_id == local_domain_id:
                    continue

                params = {
                    'domain_id': remote_domain_id,
                    'query': query
                }

                resources_message = conn_with_remote_repository['conn'].dispatch(method, params)
                resources_data = MessageToDict(resources_message, preserving_proto_field_name=True)

                if not resources_data.get('results'):
                    continue

                for resource_data in resources_data['results']:
                    resource_data['remote_repository'] = conn_with_remote_repository['remote_repository']
                    resource_data['domain_id'] = local_domain_id

                resources_data_from_remote += resources_data['results']
                total_count_from_remote += resources_data['total_count']

        if remote_repository_name:
            resources_data_from_remote, total_count_from_remote = self._filter_by_remote_repository_name(
                resources_data_from_remote,
                remote_repository_name)

        return resources_data_from_remote, total_count_from_remote

    def get_resource_from_remote_repository(self, resource: str, domain_id: str, **params):
        conns_by_remote_repository = self._create_conns_by_remote_repository()
        method = f'{resource}.get'

        local_domain_id = domain_id

        if conns_by_remote_repository:
            for conn_with_remote_repository in conns_by_remote_repository:
                remote_domain_id = conn_with_remote_repository['remote_repository']['domain_id']
                if remote_domain_id == local_domain_id:
                    continue

                params['domain_id'] = remote_domain_id

                try:
                    resource_message = conn_with_remote_repository['conn'].dispatch(method, params)
                    resource_data = MessageToDict(resource_message, preserving_proto_field_name=True)

                    resource_data['remote_repository'] = conn_with_remote_repository['remote_repository']
                    resource_data['domain_id'] = local_domain_id

                    return resource_data
                except Exception:
                    pass

        return False

    def _create_conns_by_remote_repository(self):
        conns = []
        if self.remote_repositories:
            for remote_repository in self.remote_repositories:
                conns.append({
                    'remote_repository': remote_repository,
                    'conn': self.locator.get_connector(SpaceConnector,
                                                                endpoint=remote_repository['endpoint'])
                })

        return conns

    @staticmethod
    def _pop_remote_repository_name_from_query(query: dict):
        remote_repository_name = {}
        filtered_query = copy.deepcopy(query)
        for index, filter_kv in enumerate(filtered_query['filter']):
            if filter_kv['k'] == 'remote_repository_name':
                remote_repository_name = filtered_query['filter'].pop(index)

        return filtered_query, remote_repository_name

    @staticmethod
    def _filter_by_remote_repository_name(raw_providers_data, remote_repository_name_filter):
        providers_data = copy.deepcopy(raw_providers_data)
        for index, provider_data in enumerate(providers_data):
            if provider_data['remote_repository'].get('name') != remote_repository_name_filter['v']:
                del providers_data[index]

        return providers_data, len(providers_data)

    @staticmethod
    def _remote_repository_filter(name: str, version: str, repository: dict):
        is_matched_flag = True

        if name and repository['name'] != name:
            is_matched_flag = False

        if version and repository['version'] != version:
            is_matched_flag = False

        return is_matched_flag

    @staticmethod
    def _pop_local_domain_id_from_query(raw_query):
        query = copy.deepcopy(raw_query)
        domain_id = ''

        filters = query.get('filter', [])
        for index, filter in enumerate(filters):
            key = filter['k']
            if key == 'domain_id':
                domain_id = filter.pop('v')
                del filters[index]
                query['filter'] = filters

        return query, domain_id