import os
import unittest

from google.protobuf.json_format import MessageToDict

from spaceone.core import utils, pygrpc
from spaceone.core.unittest.runner import RichTestRunner


class TestProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestProvider, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestProvider, cls).tearDownClass()

    def setUp(self):
        endpoints = {
            'repository_v2': 'localhost:50051/v1'
        }
        self.repository_v2 = pygrpc.client(endpoint=endpoints.get('repository_v2', {}))
        self.provider_info = {
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
                'identity.ServiceAccount': {
                    'field': 'contents'
                }
            },
            'schema': {
                'identity.ServiceAccount': 'aws_service_account',
                'secret.TrustedSecret': 'aws_access_key',
                'secret.Secret': [
                    'aws.assume_role'
                ]
            },
            'schema_options': {
                'trusted_service_account': 'ENABLED'
            },
            'color': 'Red',
            'icon': 's3://spaceone-custome-assets',
            'reference': {
                'identity.ServiceAccount': {
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

        self.sync_mode = {
            'UNDEFINED': 0,
            'NONE': 1,
            'MANUAL': 2,
            'AUTOMATIC': 3,
        }

    def tearDown(self):
        print(f"[TEARDOWN] delete {self.provider_info['provider']} in {self.provider_info['domain_id']}")
        self.repository_v2.Provider.delete({
            'domain_id': self.provider_info['domain_id'],
            'provider': self.provider_info['provider']
        })

    def test_create_provider(self):
        params = self.provider_info

        self.provider = self.repository_v2.Provider.create(params)

        self.assertEqual(self.provider.name, params['name'])
        self.assertEqual(self.provider.provider, params['provider'])
        self.assertEqual(self.provider.domain_id, params['domain_id'])
        self.assertEqual(self.provider.sync_mode, self.sync_mode[params['sync_mode']])
        self.assertDictEqual(MessageToDict(self.provider.sync_options), params['sync_options'])
        self.assertDictEqual(MessageToDict(self.provider.description), params['description'])
        self.assertDictEqual(MessageToDict(self.provider.schema), params['schema'])
        self.assertDictEqual(MessageToDict(self.provider.schema_options), params['schema_options'])
        self.assertEqual(self.provider.color, params['color'])
        self.assertEqual(self.provider.icon, params['icon'])
        self.assertDictEqual(MessageToDict(self.provider.reference), params['reference'])
        self.assertListEqual(MessageToDict(self.provider.labels), params['labels'])# How about variable has list type?
        self.assertDictEqual(MessageToDict(self.provider.tags), params['tags'])

    def test_get_provider(self):
        self.test_create_provider()

        provider = self.repository_v2.Provider.get({
            'domain_id': self.provider_info['domain_id'],
            'provider': self.provider_info['provider']
        })

        self.assertEqual(provider.name, self.provider_info['name'])
        self.assertEqual(provider.provider, self.provider_info['provider'])
        self.assertEqual(provider.domain_id, self.provider_info['domain_id'])

    def test_update_provider(self):
        self.test_create_provider()

        provider = self.repository_v2.Provider.update({
            'domain_id': self.provider_info['domain_id'],
            'provider': self.provider_info['provider'],
            'name': utils.random_string(2),
        })
        self.assertNotEqual(provider.name, self.provider_info['name'])

    def test_list_provider(self):
        self.test_create_provider()

        for param in ['name', 'provider', 'sync_mode']:
            providers = self.repository_v2.Provider.list({
                'domain_id': self.provider_info['domain_id'],
                param: self.provider_info[param]
            })

            self.assertEqual(providers.total_count, 1)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
