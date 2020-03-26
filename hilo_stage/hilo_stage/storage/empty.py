from tfx.types import Channel, channel_utils

from hilo_stage.storage.config import InputConfig, EmptyConfig
from hilo_stage.storage.input import Input


class Empty(Input):
    """Empty implements an empty input. It returns an empty channel"""
    def __init__(self, config: EmptyConfig):
        super().__init__(InputConfig(empty=config))

    def channel(self) -> Channel:
        return channel_utils.as_channel([])