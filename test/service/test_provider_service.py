import unittest
import copy

from unittest.mock import patch
from mongoengine import connect, disconnect

from google.protobuf.json_format import MessageToDict
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.model.mongo_model import MongoModel
from spaceone.core.transaction import Transaction
from cloudforet.repository.service.provider_service import ProviderService
from cloudforet.repository.info.provider_info import ProviderInfo
from cloudforet.repository.error.provider import *


class TestProviderService(unittest.TestCase):
    base_params = {
        'provider': 'aws',
        'name': utils.random_string(2),
        'sync_mode': 'AUTOMATIC',
        'sync_options': {
            'source_type': 'GITHUB',
            'source': {
                'url': 'https://github.com/cloudforet-io/managed-repository-resources.git',
                'path': '/provider/aws.yaml',
                'secret_data': {
                    'token': 'token'
                }
            }
        },
        'description': {
            'identitydotServiceAccount': {
                'field': 'contents'
            }
        },
        'schema': {
            'identitydotServiceAccount': 'aws_service_account',
            'secretdotTrustedSecret': 'aws_access_key',
            'secretdotSecret': [
                'aws_assume_role'
            ]
        },
        'capability': {
            'trusted_service_account': 'ENABLED'
        },
        'color': 'Red',
        'icon': 's3://spaceone-custome-assets',
        'reference': {
            'identitydotServiceAccount': {
                'Link': 'template'
            }
        },
        'labels': [
            'label_1',
            'label_2',
        ],
        'tags': {
            'key': 'value'
        },
        'domain_id': f'domain-{utils.random_string()}',
    }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='cloudforet.repository')
        config.set_service_config()
        config.set_global(MOCK_MODE=True)
        connect('test', host='mongomock://localhost')

        cls.transaction = Transaction({
            'service': 'repository',
            'api_class': 'Provider'
        })

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    @patch.object(MongoModel, 'connect', return_value=None)
    def tearDown(self, *args) -> None:
        print('(tearDown) Nothing to do')
        pass

    def test_create_provider(self, *args):
        params = self.base_params
        sync_mode = {
            'UNDEFINED': 0,
            'NONE': 1,
            'MANUAL': 2,
            'AUTOMATIC': 3,
        }

        self.transaction.method = 'create'
        provider_svc = ProviderService(transaction=self.transaction)
        provider_vo = provider_svc.create(params.copy())
        provider_info = ProviderInfo(provider_vo)

        self.assertEqual(provider_info.name, params['name'])
        self.assertEqual(provider_info.provider, params['provider'])
        self.assertEqual(provider_info.domain_id, params['domain_id'])
        self.assertEqual(provider_info.sync_mode, sync_mode[params['sync_mode']])
        self.assertDictEqual(MessageToDict(provider_info.sync_options, preserving_proto_field_name=True),
                             params['sync_options'])
        self.assertDictEqual(MessageToDict(provider_info.description), params['description'])
        self.assertDictEqual(MessageToDict(provider_info.schema), params['schema'])
        self.assertDictEqual(MessageToDict(provider_info.capability, preserving_proto_field_name=True),
                             params['capability'])
        self.assertEqual(provider_info.color, params['color'])
        self.assertEqual(provider_info.icon, params['icon'])
        self.assertDictEqual(MessageToDict(provider_info.reference), params['reference'])
        self.assertListEqual(MessageToDict(provider_info.labels), params['labels'])
        self.assertDictEqual(MessageToDict(provider_info.tags), params['tags'])

    def test_create_fail_provider(self, *args):
        params = copy.deepcopy(self.base_params)

        params['sync_options']['source_type'] = 'GITLAB'
        params['domain_id'] = f'domain-{utils.random_string()}'
        with self.assertRaises(ERROR_INVALID_SOURCE_TYPE):
            self.transaction.method = 'create'
            provider_svc = ProviderService(transaction=self.transaction)
            provider_svc.create(params.copy())

        params['sync_options']['source_type'] = 'GITHUB'
        params['domain_id'] = f'domain-{utils.random_string()}'
        del params['sync_options']['source']
        with self.assertRaises(ERROR_INSUFFICIENT_SYNC_OPTIONS):
            self.transaction.method = 'create'
            provider_svc = ProviderService(transaction=self.transaction)
            provider_svc.create(params.copy())

        for mode in ['MANUAL', 'AUTOMATIC']:
            params['sync_mode'] = mode
            params['sync_options'] = {}
            params['domain_id'] = f'domain-{utils.random_string()}'
            with self.assertRaises(ERROR_INSUFFICIENT_SYNC_OPTIONS):
                self.transaction.method = 'create'
                provider_svc = ProviderService(transaction=self.transaction)
                provider_svc.create(params.copy())



    def test_get_provider(self, *args):
        params = {
            'domain_id': self.base_params['domain_id'],
            'provider': self.base_params['provider']
        }

        self.transaction.method = 'get'
        provider_svc = ProviderService(transaction=self.transaction)
        provider_vo = provider_svc.get(params.copy())

        self.assertEqual(provider_vo.provider, params['provider'])
        self.assertEqual(provider_vo.domain_id, params['domain_id'])

    def test_update_provider(self, *args):
        params = {
            'name': utils.random_string(2),
            'domain_id': self.base_params['domain_id'],
            'provider': self.base_params['provider']
        }

        self.transaction.method = 'update'
        provider_svc = ProviderService(transaction=self.transaction)
        provider_vo = provider_svc.update(params.copy())

        self.assertEqual(provider_vo.name, params['name'])
        self.assertEqual(provider_vo.provider, params['provider'])
        self.assertEqual(provider_vo.domain_id, params['domain_id'])

    def test_list_provider(self, *args):
        params = {
            'domain_id': self.base_params['domain_id']
        }

        self.transaction.method = 'list'
        provider_svc = ProviderService(transaction=self.transaction)
        provider_vos, total_count = provider_svc.list(params.copy())

        self.assertEqual(total_count, 1)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
