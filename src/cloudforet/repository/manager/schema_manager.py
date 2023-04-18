import logging

from spaceone.core.manager import BaseManager
from cloudforet.repository.model.schema_model import Schema

_LOGGER = logging.getLogger(__name__)


class SchemaManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_model: Schema = self.locator.get_model(Schema)

    def create_schema(self, params: dict):
        def _rollback(schema_vo: Schema):
            _LOGGER.info(f'[ROLLBACK] Delete schema : {schema_vo.schema_id}')
            schema_vo.delete()

        schema_vo: Schema = self.schema_model.create(params)
        self.transaction.add_rollback(_rollback, schema_vo)

        schema_data = schema_vo.to_dict()
        return schema_data

    def update_schema(self, params: dict):
        schema_vo: Schema = self.get_schema(params['schema_id'], params['domain_id'])

        return self.update_schema_by_vo(params, schema_vo)

    def update_schema_by_vo(self, params, schema_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[ROLLBACK] Update schema : {schema_vo.schema_id}')
            schema_vo.delete(old_data)

        self.transaction.add_rollback(_rollback, schema_vo.to_dict())

        schema_data = schema_vo.update(params).to_dict()
        return schema_data

    def delete_schema(self, params: dict):
        schema_vo: Schema = self.get_schema(params['schema_id'], params['domain_id'])
        schema_vo.delete()

    def get_schema(self, schema_id: str, domain_id: str, only=None):
        return self.schema_model.get(schema_id=schema_id, domain_id=domain_id, only=only)

    def filter_schemas(self, **conditions):
        return self.schema_model.filter(**conditions)

    def list_schemas(self, query: dict):
        for _, filter in enumerate(query['filter']):
            if filter['k'] == 'remote_repository_name':
                return [], 0

        schema_vos, total_count = self.schema_model.query(**query)

        return schema_vos, total_count

    def stat_schema(self, query):
        return self.schema_model.stat(**query)
