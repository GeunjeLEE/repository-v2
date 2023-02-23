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
            'description': Description(provider_vo.description),
            'schema': Schema(provider_vo.schema),
            'capability': Capability(provider_vo.capability),
            'color': provider_vo.color,
            'icon': provider_vo.icon,
            'reference': Refernece(provider_vo.reference),
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


def Schema(schema):
    if schema:
        array_of_object = []
        for schema_vo in schema:
            info = {
                'resource_type': schema_vo.resource_type,
                'secret_type': schema_vo.secret_type,
                'schema_id': schema_vo.schema_id
            }
            array_of_object.append(provider_pb2.Schema(**info))

        return array_of_object

    return None


def Capability(capability):
    if capability:
        info = {
            'trusted_service_account': capability.trusted_service_account
        }
        return provider_pb2.Capability(**info)

    return None


def Description(description):
    if description:
        array_of_object = []
        for description_vo in description:
            info = {
                'resource_type': description_vo.resource_type,
                'body': description_vo.body
            }
            array_of_object.append(provider_pb2.Description(**info))

        return array_of_object

    return None


def Refernece(reference):
    if reference:
        array_of_object = []
        for reference_vo in reference:
            info = {
                'resource_type': reference_vo.resource_type,
                'link': reference_vo.link,
            }
            array_of_object.append(provider_pb2.Reference(**info))

        return array_of_object

    return None
