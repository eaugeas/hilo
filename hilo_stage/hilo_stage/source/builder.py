from typing import Optional

from tfx.types import Channel

from hilo_rpc.proto.source_pb2 import Source
from hilo_rpc.proto.connector_pb2 import ConnectorConfig
from hilo_stage.connector.builder import Builder as ConnectorBuilder


class Builder(object):
    """Builder creates an instance of a Channel from the Source
    description"""
    def __init__(self, source: Optional[Source] = None):
        self._source = source or Source()

    def _connector_config(self) -> ConnectorConfig:
        if self._source.config.WhichOneof('config') == 'empty':
            return ConnectorConfig(empty=self._source.config.empty)
        elif self._source.config.WhichOneof('config') == 'local_file':
            return ConnectorConfig(local_file=self._source.config.local_file)
        else:
            raise ValueError('Unknown source config type {0}'.format(
                self._source.config))

    def build(self) -> Channel:
        config = self._connector_config()
        return ConnectorBuilder(config).build()
