from spaceone.api.repository.v2 import provider_pb2, provider_pb2_grpc
from spaceone.core.pygrpc import BaseAPI
from cloudforet.repository.service.provider_service import ProviderService
from cloudforet.repository.info.provider_info import ProviderInfo, ProvidersInfo
from cloudforet.repository.info.common_info import EmptyInfo


class Provider(BaseAPI, provider_pb2_grpc.ProviderServicer):

    pb2 = provider_pb2
    pb2_grpc = provider_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(ProviderService, metadata) as provider_svc:
            provider_data = provider_svc.create(params)
            return self.locator.get_info(ProviderInfo, provider_data)

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(ProviderService, metadata) as provider_svc:
            provider_data = provider_svc.update(params)
            return self.locator.get_info(ProviderInfo, provider_data)

    def sync(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(ProviderService, metadata) as provider_svc:
            provider_data = provider_svc.sync(params)
            return self.locator.get_info(ProviderInfo, provider_data)

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(ProviderService, metadata) as provider_svc:
            provider_svc.delete(params)
            return self.locator.get_info(EmptyInfo)

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(ProviderService, metadata) as provider_svc:
            provider_data = provider_svc.get(params)
            return self.locator.get_info(ProviderInfo, provider_data)

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service(ProviderService, metadata) as provider_svc:
            providers_data, total_count = provider_svc.list(params)
            return self.locator.get_info(ProvidersInfo, providers_data, total_count, minimal=self.get_minimal(params))
