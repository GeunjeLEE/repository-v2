import functools
import logging

from spaceone.api.repository.v2 import provider_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils
from cloudforet.repository.model.provider_model import Provider

_LOGGER = logging.getLogger(__name__)


def ProviderInfo(provider_vo: Provider, minimal=False):
    info = {
        'provider': provider_vo.provider,
        'name': provider_vo.name,
        'sync_mode': provider_vo.sync_mode,
    }

    if not minimal:
        info.update({
            'sync_options': SyncOptions(provider_vo.sync_options),
            'description': change_struct_type(provider_vo.description),
            'schema': change_struct_type(provider_vo.schema),
            'capability': Capability(provider_vo.capability),
            'color': provider_vo.color,
            'icon': provider_vo.icon,
            'reference': change_struct_type(provider_vo.reference),
            'labels': change_list_value_type(provider_vo.labels),
            'tags': change_struct_type(provider_vo.tags),
            'domain_id': provider_vo.domain_id,
            'created_at': utils.datetime_to_iso8601(provider_vo.created_at),
        })

    return provider_pb2.ProviderInfo(**info)


def ProvidersInfo(provider_vos: Provider, total_count, **kwargs):
    return provider_pb2.ProvidersInfo(results=list(map(functools.partial(ProviderInfo, **kwargs), provider_vos)),
                                      total_count=total_count)


def SyncOptions(sync_options):
    if sync_options:
        info = {
            'source_type': sync_options.source_type,
            'source': change_struct_type(sync_options.source),
        }
        return provider_pb2.SyncOptions(**info)

    return None


def Capability(capability):
    if capability:
        info = {
            'trusted_service_account': capability.trusted_service_account
        }
        return provider_pb2.Capability(**info)

    return None
