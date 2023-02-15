from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel

__all__ = ['Provider']


class Provider(MongoModel):
    provider = StringField(max_length=40, required=True, unique_with='domain_id')
    name = StringField(max_length=255, required=True)
    sync_mode = StringField(default='NONE', choices=('NONE', 'MANUAL', 'AUTOMATIC'))
    sync_options = DictField()
    description = DictField()
    schema = DictField()
    schema_options = DictField()
    color = StringField(max_length=7, default=None, null=True)
    icon = StringField(max_length=255, default=None, null=True)
    reference = DictField()
    labels = ListField(StringField(max_length=255))
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
