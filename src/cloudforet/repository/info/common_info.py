from google.protobuf.empty_pb2 import Empty
from spaceone.core.pygrpc.message_type import *
from spaceone.api.repository.v2 import common_pb2


def EmptyInfo():
    return Empty()


def StatisticsInfo(result):
    return change_struct_type(result)


def AnalyzeInfo(result):
    return change_struct_type(result)


def SyncOptions(sync_options):
    if 'github' in sync_options.keys():
        info = {
            'github': {
                'url': sync_options.get('source_type')
            }
        }
        return common_pb2.SyncOptions(**info)

    return None
