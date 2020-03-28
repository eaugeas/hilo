from typing import Optional

from tfx.types import Channel

from hilo_rpc.proto.source_pb2 import Source
from hilo_stage.storage.build import input_from_config


class Builder(object):
    def __init__(self, source: Optional[Source] = None):
        self._source = source or Source()

    def build(self) -> Channel:
        input = input_from_config(self._source.config)
        return input.channel()
