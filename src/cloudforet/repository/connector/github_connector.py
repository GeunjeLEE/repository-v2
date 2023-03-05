import logging

from github import Github
from github.GithubException import GithubException
from spaceone.core.connector import BaseConnector
from spaceone.core import config
from cloudforet.repository.error.provider import *

__all__ = ["GitHubConnector"]

_LOGGER = logging.getLogger(__name__)


class GitHubConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.github_client = Github()
        self.github_read_token = config.get_global('GITHUB_READ_TOKEN', '')

    def get_file(self, repo_name: str, path: str):
        if self.github_read_token:
            self.github_client.__init__(password=self.github_read_token)

        try:
            repo = self.github_client.get_repo(repo_name)
            return repo.get_contents(path).decoded_content
        except GithubException as e:
            raise ERROR_CONNECTOR(connector='GithubConnector', reason=e)

    def create_webhook(self, github_config: dict):
        pass
        # TODO: phase 3
        # token = github_config['token']
        # repo_name = github_config['repo_name']
        # webhook_url = github_config['webhook_url']
        # events = ["create"]
        #
        # webhook_config = {
        #     'url': webhook_url,
        #     'content_type': "json"
        # }
        #
        # try:
        #     self.github_client.__init__(password=token)
        #     repo = self.github_client.get_repo(repo_name)
        #     repo.create_hook('web', webhook_config, events, active=True)
        # except GithubException as e:
        #     raise ERROR_CONNECTOR(connector='GithubConnector', reason=e)
