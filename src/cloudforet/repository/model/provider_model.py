from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel

__all__ = ['Provider']


class SyncOptions(EmbeddedDocument):
    source_type = StringField()
    source = DictField()


class Capability(EmbeddedDocument):
    trusted_service_account = StringField(default='DISABLED', choices=('ENABLED', 'DISABLED'))


class Schema(EmbeddedDocument):
    resource_type = StringField()
    secret_type = StringField()
    schema_id = StringField()


class Description(EmbeddedDocument):
    resource_type = StringField()
    body = DictField()


class Reference(EmbeddedDocument):
    resource_type = StringField()
    link = DictField()


class Provider(MongoModel):
    provider = StringField(max_length=40, required=True, unique_with='domain_id')
    name = StringField(max_length=255, required=True)
    sync_mode = StringField(default='NONE', choices=('NONE', 'MANUAL', 'AUTOMATIC'))
    sync_options = EmbeddedDocumentField(SyncOptions, default={})
    description = EmbeddedDocumentListField(Description, default=None)
    schema = EmbeddedDocumentListField(Schema, default=None)
    capability = EmbeddedDocumentField(Capability, default=None)
    color = StringField(max_length=7, default=None, null=True)
    icon = StringField(max_length=255, default=None, null=True)
    reference = EmbeddedDocumentListField(Reference, default=None)
    labels = ListField(StringField(max_length=255))
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
