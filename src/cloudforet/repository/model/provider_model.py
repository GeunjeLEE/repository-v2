from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel

__all__ = ['Provider']


class SyncOptions(EmbeddedDocument):
    source_type = StringField()
    source = DictField(default={})


class Capability(EmbeddedDocument):
    trusted_service_account = StringField(default='DISABLED', choices=('ENABLED', 'DISABLED'))


class Provider(MongoModel):
    provider = StringField(max_length=40, required=True, unique_with='domain_id')
    name = StringField(max_length=255, required=True)
    sync_mode = StringField(default='NONE', choices=('NONE', 'MANUAL', 'AUTOMATIC'))
    sync_options = EmbeddedDocumentField(SyncOptions, default=None)
    description = DictField()
    schema = DictField()
    capability = EmbeddedDocumentField(Capability, default=None)
    color = StringField(max_length=7, default=None, null=True)
    icon = StringField(max_length=255, default=None, null=True)
    reference = DictField()
    labels = ListField(StringField(max_length=255))
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
