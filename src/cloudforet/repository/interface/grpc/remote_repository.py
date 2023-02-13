from spaceone.api.repository.v2 import remote_repository_pb2, remote_repository_pb2_grpc
from spaceone.core.pygrpc import BaseAPI
from cloudforet.repository.service.remote_repository_service import RemoteRepositoryService
from cloudforet.repository.info.remote_repository_info import RemoteRepositoryInfo, RemoteRepositoriesInfo


class RemoteRepository(BaseAPI, remote_repository_pb2_grpc.RemoteRepositoryServicer):

    pb2 = remote_repository_pb2
    pb2_grpc = remote_repository_pb2_grpc

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(RemoteRepositoryService, metadata) as remote_repository_svc:
            remote_repository_vo = remote_repository_svc.get(params)
            return self.locator.get_info(RemoteRepositoryInfo, remote_repository_vo)

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(RemoteRepositoryService, metadata) as remote_repository_svc:
            remote_repository_vos, total_count = remote_repository_svc.list(params)
            return self.locator.get_info(RemoteRepositoriesInfo, total_count)
