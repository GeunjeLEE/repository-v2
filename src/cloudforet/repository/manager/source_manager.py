import logging
import yaml

from spaceone.core.manager import BaseManager
from cloudforet.repository.connector.source_connector.github_connector import GitHubConnector

_LOGGER = logging.getLogger(__name__)
_SOURCE_CONNECTOR_MAP = {
    'github': GitHubConnector
}


class SourceManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_source(self, source_type: str, repo_name: str, path: str):
        connector = self.locator.get_connector(_SOURCE_CONNECTOR_MAP[source_type])
        provider_source = connector.get_source(repo_name, path)
        provider_yaml = provider_source.decode('utf-8')

        return yaml.load(provider_yaml, Loader=yaml.Loader)

    def create_webhook(self, config: dict):
        # TODO: phase 3
        pass
        # self.github_connector.create_webhook(config)
