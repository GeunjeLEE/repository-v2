import logging
import jsonschema

from jsonschema.exceptions import ValidationError
from spaceone.core.service import *
from cloudforet.repository.manager.schema_manager import SchemaManager
from cloudforet.repository.manager.remote_repository_manager import RemoteRepositoryManager
from cloudforet.repository.manager.source_manager import SourceManager
from cloudforet.repository.error.schema import *
from cloudforet.repository.error.sync import *
from cloudforet.repository.libs.sync_utils import validate_sync_mode, parse_source_url, validate_params_data_schema

_LOGGER = logging.getLogger(__name__)


class SchemaService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_mgr: SchemaManager = self.locator.get_manager(SchemaManager)
        self.remote_repository_mgr: RemoteRepositoryManager = self.locator.get_manager(RemoteRepositoryManager)
        self.source_mgr: SourceManager = self.locator.get_manager(SourceManager)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['schema_id', 'name', 'schema', 'domain_id'])
    def create(self, params: dict):
        self._validate_json_document_schema(params['schema'])
        params, secret_data = validate_params_data_schema(params)

        if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC']:
            source_type = list(params['sync_options'].keys())[0]
            repo_name, directory, file = parse_source_url(params['sync_options'][source_type]['url'])
            path = f'{directory}/{file}'
            schema_data = self.source_mgr.get_source(source_type, repo_name, path)
            validate_params_data_schema(schema_data)
            schema_data.update(params)
            params = schema_data

        return self.schema_mgr.create_schema(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['schema_id', 'domain_id'])
    def update(self, params: dict):
        params, secret_data = validate_params_data_schema(params)
        schema_vo = self.schema_mgr.get_schema(params['schema_id'], params['domain_id'])

        return self.schema_mgr.update_schema_by_vo(params, schema_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['schema_id', 'domain_id'])
    def delete(self, params: dict):
        return self.schema_mgr.delete_schema(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['schema_id', 'domain_id'])
    def sync(self, params: dict):
        schema_vo = self.schema_mgr.get_schema(params['schema_id'], params['domain_id'])
        validate_sync_mode(schema_vo.sync_mode)

        source_type = list(schema_vo['sync_options'].keys())[0]
        repo_name, directory, file = parse_source_url(schema_vo['sync_options'][source_type]['url'])
        path = f'{directory}/{file}'
        schema_data = self.source_mgr.get_source(source_type, repo_name, path)

        schema_data, _ = validate_params_data_schema(schema_data)
        validate_sync_mode(schema_data['sync_mode'])

        return self.schema_mgr.update_schema_by_vo(schema_data, schema_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['schema_id', 'domain_id'])
    def get(self, params: dict):
        schema_vos = self.schema_mgr.filter_schemas(schema_id=params['schema_id'], domain_id=params['domain_id'])
        if schema_vos.count() == 1:
            return schema_vos[0].to_dict()
        else:
            schema_data = self.remote_repository_mgr.get_resource_from_remote_repository(
                'Schema', domain_id=params['domain_id'],
                only=params.get('only'),
                schema_id=params['schema_id']
            )

            if schema_data:
                return schema_data

        raise ERROR_NOT_FOUND(key='schema_id', value=params['schema_id'])

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['domain_id'])
    @append_query_filter(['schema_id', 'name', 'sync_mode', 'remote_repository_name', 'domain_id'])
    @append_keyword_filter(['schema_id', 'name'])
    def list(self, params: dict):
        query = params.get('query', {})

        local_schemas_vos, local_total_count = self.schema_mgr.list_schemas(query)
        local_schemas_data = []
        for local_schema_vo in local_schemas_vos:
            local_schemas_data.append(local_schema_vo.to_dict())

        remote_schemas_data, remote_total_count = self.remote_repository_mgr.list_resources_from_remote_repository(
            'Schema', query)

        schemas = local_schemas_data + remote_schemas_data
        total_count = local_total_count + remote_total_count

        return schemas, total_count

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    @append_keyword_filter(['schema_id', 'name'])
    def stat(self, params):
        query = params.get('query', {})

        return self.schema_mgr.stat_schema(query)

    @staticmethod
    def _validate_params_data_schema(params: dict):
        secret_data = {}

        if not params.get('sync_mode') or params['sync_mode'] == 'NONE':
            params['sync_options'] = {}
        else:
            if not params.get('sync_options'):
                raise ERROR_INSUFFICIENT_SYNC_OPTIONS(sync_options=params['sync_options'])

        if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC']:
            source_type = list(params['sync_options'].keys())[0]
            if params['sync_options'][source_type].get('token'):
                secret_data = params['sync_options'][source_type].pop('token')

        return params, secret_data

    @staticmethod
    def _validate_json_document_schema(schema):
        if schema:
            try:
                jsonschema.Draft7Validator.check_schema(schema)
            except ValidationError:
                raise ERROR_INVALID_SCHEMA(schema=schema)
