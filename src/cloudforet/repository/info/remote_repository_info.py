import functools
import logging

from spaceone.api.repository.v2 import remote_repository_pb2

_LOGGER = logging.getLogger(__name__)


def RemoteRepositoryInfo(remote_repository_dict: dict):
    return remote_repository_pb2.RemoteRepositoryInfo(**remote_repository_dict)


def RemoteRepositoriesInfo(remote_repository_data, total_count, **kwargs):
    return remote_repository_pb2.RemoteRepositoriesInfo(
        results=list(map(functools.partial(RemoteRepositoryInfo, **kwargs), remote_repository_data)),
        total_count=total_count
    )
