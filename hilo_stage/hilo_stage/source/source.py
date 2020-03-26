from tfx.types import Channel

from hilo_rpc.proto.source_pb2 import Source as SourceDescriptor
from hilo_stage.storage.build import input_from_config


class Source(object):
    """Source provides a channel from which stages and pipelines
    receive data.
    """
    def __init__(self, descriptor: SourceDescriptor):
        self._descriptor = descriptor
        print ('source config: ', self._descriptor.config.WhichOneof('config'))
        self._input = input_from_config(self._descriptor.config)

    @property
    def descriptor(self) -> SourceDescriptor:
        return self._descriptor

    def channel(self) -> Channel:
        return self._input.channel()
