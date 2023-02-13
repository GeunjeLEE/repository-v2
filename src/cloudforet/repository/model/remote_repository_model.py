from mongoengine import *
from spaceone.core.model.mongo_model import MongoModel

__all__ = ['RemoteRepository']


class RemoteRepository(MongoModel):
    name = StringField(max_length=255, required=True)
    description = StringField(max_length=255)
    endpoint = StringField(max_length=255)
    version = StringField(max_length=10)
