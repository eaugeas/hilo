from tfx.types import Channel
from tfx.utils.dsl_utils import external_input

from hilo_stage.storage.input import Input
from hilo_stage.storage.config import LocalFileConfig


class LocalFile(Input):
    """LocalFile is an implementation of a storage Input that
    reads from a local file
    """
    def __init__(self, config: LocalFileConfig):
        super().__init__()
        self._config = config

    @staticmethod
    def from_config(config: LocalFileConfig) -> 'LocalFile':
        return LocalFile(config)

    def channel(self) -> Channel:
        from os import path

        abspath = path.abspath(self._config.path)
        return external_input(abspath)
