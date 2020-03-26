from tfx.types import Channel

from hilo_stage.storage.config import InputConfig


class Input(object):
    """Input is an interface for classes that act as
    input data sources.
    """

    def channel(self) -> Channel:
        raise NotImplementedError()
