from tfx.types import Channel


class Input(object):
    """Input is an interface for classes that act as
    input data sources.
    """

    def channel(self) -> Channel:
        raise NotImplementedError()
