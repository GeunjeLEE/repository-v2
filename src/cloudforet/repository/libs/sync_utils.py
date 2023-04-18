from cloudforet.repository.error.sync import *


def validate_sync_mode(sync_mode: str):
    if sync_mode not in ['MANUAL', 'AUTOMATIC']:
        raise ERROR_UNSUPPORT_SYNC_MODE(sync_mode=sync_mode)


def validate_params_data_schema(params: dict):
    secret_data = {}

    if not params.get('sync_mode') or params['sync_mode'] == 'NONE':
        params['sync_options'] = {}
    else:
        if not params.get('sync_options'):
            raise ERROR_INSUFFICIENT_SYNC_OPTIONS(sync_options=params['sync_options'])

    if params.get('sync_mode') in ['MANUAL', 'AUTOMATIC']:
        source_repository = list(params['sync_options'].keys())[0]
        if params['sync_options'][source_repository].get('token'):
            secret_data = params['sync_options'][source_repository].pop('token')

    return params, secret_data


def parse_source_url(url):
    repo_name = f'{url.split("/")[0]}/{url.split("/")[1]}'
    directory = url.split("/")[2]
    file = url.split("/")[3]
    return repo_name, directory, file
