import logging
import yaml

from spaceone.core.manager import BaseManager
from cloudforet.repository.connector.github_connector import GitHubConnector

_LOGGER = logging.getLogger(__name__)


class GithubManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.github_connector: GitHubConnector = self.locator.get_connector(GitHubConnector)

    def get_provider(self, repo_name: str, path: str):
        provider_file_contents = self.github_connector.get_file(repo_name, path)
        provider_yaml = provider_file_contents.decode('utf-8')

        return yaml.load(provider_yaml, Loader=yaml.Loader)

    def create_webhook(self, config: dict):
        # TODO: phase 3
        pass
        # self.github_connector.create_webhook(config)
