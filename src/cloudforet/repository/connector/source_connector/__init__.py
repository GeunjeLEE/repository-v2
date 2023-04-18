import logging
from abc import abstractmethod

from spaceone.core.connector import BaseConnector

__all__ = ['SourceConnector']
_LOGGER = logging.getLogger(__name__)


class SourceConnector(BaseConnector):

    @abstractmethod
    def get_source(self, repo_name, path):
        pass
