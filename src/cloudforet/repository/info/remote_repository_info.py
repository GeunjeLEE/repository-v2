import functools
import logging

from spaceone.api.repository.v2 import remote_repository_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils
from cloudforet.repository.model.remote_repository_model import RemoteRepository

_LOGGER = logging.getLogger(__name__)


def RemoteRepositoryInfo(remote_repository_vo: RemoteRepository):
    info = {
        'name': remote_repository_vo.name,
        'description': remote_repository_vo.description,
        'endpoint': remote_repository_vo.endpoint,
        'version': remote_repository_vo.version,
    }

    return remote_repository_pb2.RemoteRepositoryInfo(**info)


def RemoteRepositoriesInfo(remote_repository_vo: RemoteRepository, total_count, **kwargs):
    return remote_repository_pb2.RemoteRepositoryInfo(result=list(map(functools.partial(RemoteRepositoryInfo, **kwargs),
                                                                      remote_repository_vo)), total_count=total_count)
