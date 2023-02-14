import functools
import logging

from spaceone.api.repository.v2 import remote_repository_pb2

_LOGGER = logging.getLogger(__name__)


def RemoteRepositoryInfo(remote_repository_dict: dict):
    info = {
        'name': remote_repository_dict['name'],
        'description': remote_repository_dict['description'],
        'endpoint': remote_repository_dict['endpoint'],
        'version': remote_repository_dict['version'],
    }

    return remote_repository_pb2.RemoteRepositoryInfo(**info)


def RemoteRepositoriesInfo(remote_repository_data, total_count, **kwargs):
    return remote_repository_pb2.RemoteRepositoriesInfo(
        results=list(map(functools.partial(RemoteRepositoryInfo, **kwargs), remote_repository_data)),
        total_count=total_count
    )
