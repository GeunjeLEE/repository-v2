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
            'sync_mode': 'MANUAL',
            'sync_options': {
                'github': {
                    'url': 'GJ-playgroud/managed-repository-resources/aws/provider.yaml'
                    }
                },
            'description': [
                {
                    'resource_type': 'identity.ServiceAccount',
                    'body': {}
                }
            ],
            'schema': [
                {
                    'resource_type': 'identity.ServiceAccount',
                    'schema_id': 'aws-service-account'
                },
                {
                    'resource_type': 'secret.TrustedSecret',
                    'schema_id': 'aws-access-key'
                },
                {
                    'resource_type': 'secret.Secret',
                    'secret_type': 'GENERAL',
                    'schema_id': 'aws-access-key'
                },
                {
                    'resource_type': 'secret.Secret',
                    'secret_type': 'TRUSTED',
                    'schema_id': 'aws-assume-role'
                },
            ],
            'capability': {
                'trusted_service_account': 'ENABLED'
            },
            'color': 'Red',
            'icon': 's3://spaceone-custom-assets',
            'reference': [
                {
                    'resource_type': 'identity.ServiceAccount',
                    'link': {}
                }
            ],
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
            'provider': self.provider_info['provider'],
            'domain_id': self.provider_info['domain_id'],
        })

    def test_create_provider(self):
        params = self.provider_info

        provider = self.repository_v2.Provider.create(params)

        self.assertEqual(provider.name, params['name'])

    def test_get_provider(self):
        self.test_create_provider()

        provider = self.repository_v2.Provider.get({
            'domain_id': self.provider_info['domain_id'],
            'provider': self.provider_info['provider']
        })

        self.assertEqual(provider.name, self.provider_info['name'])
        self.assertEqual(provider.provider, self.provider_info['provider'])
        self.assertEqual(provider.domain_id, self.provider_info['domain_id'])

    def test_get_provider_from_remote(self):
        self.test_create_provider()

        provider = self.repository_v2.Provider.get({
            'domain_id': self.provider_info['domain_id'],
            'provider': 'google'
        })

        self.assertEqual(provider.provider, 'google')
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

        providers = self.repository_v2.Provider.list({
            'domain_id': self.provider_info['domain_id'],
        })

        self.assertEqual(providers.total_count, 2)

    def test_list_provider_by_filter(self):
        self.test_create_provider()

        for param in ['name', 'provider', 'sync_mode']:
            providers = self.repository_v2.Provider.list({
                'domain_id': self.provider_info['domain_id'],
                param: self.provider_info[param]
            })

            self.assertEqual(providers.total_count, 1)

    def test_list_provider_by_repository_name(self):
        self.test_create_provider()


        providers = self.repository_v2.Provider.list({
            'domain_id': self.provider_info['domain_id'],
            'remote_repository_name': 'remote_repository_exam_1'
        })

        self.assertEqual(providers.total_count, 1)

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
