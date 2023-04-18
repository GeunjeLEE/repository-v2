from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel

__all__ = ['Schema']


class Schema(MongoModel):
    schema_id = StringField(max_length=40, required=True, unique_with='domain_id')
    name = StringField(max_length=255, required=True)
    sync_mode = StringField(default='NONE', choices=('NONE', 'MANUAL', 'AUTOMATIC'))
    sync_options = DictField()
    schema = DictField(required=True)
    labels = ListField(StringField(max_length=255))
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
