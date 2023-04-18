import functools
import logging

from spaceone.api.repository.v2 import schema_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils
from cloudforet.repository.model.schema_model import Schema
from cloudforet.repository.info.common_info import SyncOptions

_LOGGER = logging.getLogger(__name__)


def SchemaInfo(schema_data: Schema, minimal=False):
    info = {
        'schema_id': schema_data['schema_id'],
        'name': schema_data['name'],
        'sync_mode': schema_data.get('sync_mode')
    }

    if not minimal:
        info.update({
            'sync_options': SyncOptions(schema_data.get('sync_options')),
            'schema': change_struct_type(schema_data.get('schema')),
            'labels': change_list_value_type(schema_data.get('labels')),
            'tags': change_struct_type(schema_data.get('tags')),
            'domain_id': schema_data['domain_id'],
            'created_at': utils.datetime_to_iso8601(schema_data['created_at']),
            'remote_repository': change_struct_type(schema_data.get('remote_repository')),
        })

    return schema_pb2.SchemaInfo(**info)


def SchemasInfo(schemas_data: Schema, total_count, **kwargs):
    return schema_pb2.SchemasInfo(results=list(map(functools.partial(SchemaInfo, **kwargs), schemas_data)),
                                  total_count=total_count)
