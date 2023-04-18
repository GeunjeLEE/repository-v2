import unittest

from google.protobuf.json_format import MessageToDict

from spaceone.core import utils, pygrpc
from spaceone.core.unittest.runner import RichTestRunner


class TestRemoteRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestRemoteRepository, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestRemoteRepository, cls).tearDownClass()

    def setUp(self):
        endpoints = {
            'repository_v2': 'localhost:50051/v1'
        }
        self.repository_v2 = pygrpc.client(endpoint=endpoints.get('repository_v2', {}))

    def tearDown(self):
        pass

    def test_list_remote_repository(self):
        params = {}

        # repositories = self.repository_v2.RemoteRepository.list(params)
        # print(repositories.total_count)
        # self.assertEqual(repositories.total_count, 4)
        #
        # params['name'] = 'remote_repository_exam_1' # Add condition to find repository matching name
        # repositories = self.repository_v2.RemoteRepository.list(params)
        # print(repositories.total_count)
        # self.assertEqual(repositories.total_count, 2)

        params['version'] = '1'                     # Add condition to find repository matching namd and version
        repositories = self.repository_v2.RemoteRepository.list(params)
        print(repositories)
        self.assertEqual(repositories.total_count, 1)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
