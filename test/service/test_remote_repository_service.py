import unittest
from unittest.mock import patch
from mongoengine import connect, disconnect

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.model.mongo_model import MongoModel
from spaceone.core.transaction import Transaction
from cloudforet.repository.service.remote_repository_service import RemoteRepositoryService
from cloudforet.repository.manager.remote_repository_manager import RemoteRepositoryManager


remote_repositories_conf = [
    {
        'name': 'remote_repository_exam_1',
        'description': 'A temporary repo',
        'endpoint': 'https://remote.repository.example.com',
        'version': '1'
    },
    {
        'name': 'remote_repository_exam_2',
        'description': 'A temporary repo 2',
        'endpoint': 'https://remote-2.repository.example.com',
        'version': '2'
    },
    {
        'name': 'remote_repository_exam_1',
        'description': 'A temporary repo 2',
        'endpoint': 'https://remote-2.repository.example.com',
        'version': '2'
    },
    {
        'name': 'remote_repository_exam_2',
        'description': 'A temporary repo 2',
        'endpoint': 'https://remote-2.repository.example.com',
        'version': '1'
    }
]


class TestRemoteRepositoryService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        config.init_conf(package='cloudforet.repository')
        config.set_service_config()
        config.set_global(MOCK_MODE=True)
        connect('test', host='mongomock://localhost')

        cls.transaction = Transaction({
            'service': 'repository',
            'api_class': 'RemoteRepository'
        })

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    @patch.object(MongoModel, 'connect', return_value=None)
    def tearDown(self, *args) -> None:
        print('(tearDown) Nothing to do')
        pass

    @patch.object(RemoteRepositoryManager, 'get_remote_repository', return_value=remote_repositories_conf[0])
    def test_get_remote_repository(self, *args):
        params = {
            'name': 'remote_repository_exam_1'
        }

        self.transaction.method = 'get'
        re_repo_svc = RemoteRepositoryService(transaction=self.transaction)
        re_repo_dict = re_repo_svc.get(params.copy())

        print(re_repo_dict)
        self.assertEqual(re_repo_dict['name'], remote_repositories_conf[0]['name'])

    @patch.object(RemoteRepositoryManager, 'list_remote_repositories', return_value=(remote_repositories_conf,
                                                                                     len(remote_repositories_conf)))
    def test_list_remote_repository(self, *args):
        params = {}

        self.transaction.method = 'list'
        re_repo_svc = RemoteRepositoryService(transaction=self.transaction)
        re_repo_list_of_dict, total_count = re_repo_svc.list(params)

        print(re_repo_list_of_dict)
        self.assertEqual(total_count, len(remote_repositories_conf))


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
