import functools
import logging

from spaceone.api.repository.v2 import provider_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils
from cloudforet.repository.model.provider_model import Provider

_LOGGER = logging.getLogger(__name__)


def ProviderInfo(provider_data: Provider, minimal=False):
    info = {
        'provider': provider_data['provider'],
        'name': provider_data['name'],
        'sync_mode': provider_data.get('sync_mode'),
    }

    if not minimal:
        info.update({
            'sync_options': SyncOptions(provider_data.get('sync_options')),
            'description': Description(provider_data.get('description')),
            'schema': Schema(provider_data.get('schema')),
            'capability': Capability(provider_data.get('capability')),
            'color': provider_data.get('color'),
            'icon': provider_data.get('icon'),
            'reference': Refernece(provider_data.get('reference')),
            'labels': change_list_value_type(provider_data.get('labels')),
            'tags': change_struct_type(provider_data.get('tags')),
            'domain_id': provider_data['domain_id'],
            'created_at': utils.datetime_to_iso8601(provider_data['created_at']),
            'remote_repository': change_struct_type(provider_data.get('remote_repository')),
        })

    return provider_pb2.ProviderInfo(**info)


def ProvidersInfo(provider_datas: Provider, total_count, **kwargs):
    return provider_pb2.ProvidersInfo(results=list(map(functools.partial(ProviderInfo, **kwargs), provider_datas)),
                                      total_count=total_count)


def SyncOptions(sync_options):
    if sync_options:
        info = {
            'source_type': sync_options.get('source_type'),
            'source': change_struct_type(sync_options.get('source')),
        }
        return provider_pb2.SyncOptions(**info)

    return None


def Schema(schema):
    if schema:
        list_of_dict = []
        for schema_vo in schema:
            info = {
                'resource_type': schema_vo.get('resource_type'),
                'secret_type': schema_vo.get('secret_type'),
                'schema_id': schema_vo.get('schema_id'),
            }
            list_of_dict.append(provider_pb2.Schema(**info))

        return list_of_dict

    return None


def Capability(capability):
    if capability:
        info = {
            'trusted_service_account': capability.get('trusted_service_account')
        }
        return provider_pb2.Capability(**info)

    return None


def Description(description):
    if description:
        list_of_dict = []
        for description_vo in description:
            info = {
                'resource_type': description_vo.get('resource_type'),
                'body': description_vo.get('body'),
            }
            list_of_dict.append(provider_pb2.Description(**info))

        return list_of_dict

    return None


def Refernece(reference):
    if reference:
        list_of_dict = []
        for reference_vo in reference:
            info = {
                'resource_type': reference_vo.get('resource_type'),
                'link': reference_vo.get('link'),
            }
            list_of_dict.append(provider_pb2.Reference(**info))

        return list_of_dict

    return None
