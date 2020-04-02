from typing import Optional

from tfx.types import Channel

from hilo_rpc.proto.source_pb2 import Source
from hilo_stage.connector.builder import Builder as ConnectorBuilder


class Builder(object):
    """Builder creates an instance of a Channel from the Source
    description"""
    def __init__(self, source: Optional[Source] = None):
        self._source = source or Source()

    def build(self) -> Channel:
        return ConnectorBuilder(self._source.config).build()
