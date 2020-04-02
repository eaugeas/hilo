from typing import Any, Dict, Optional, Text, Type

from tfx.types import Channel, channel_utils

from hilo_stage.connector.config import (
    ConnectorConfig, EmptyConfig, LocalFileConfig)


class ConnectorBuilder(object):
    def __init__(self, any: Any):
        pass

    def build(self) -> Channel:
        raise NotImplementedError()


class EmptyBuilder(ConnectorBuilder):
    """Empty implements an empty input. It builds an empty channel"""
    def __init__(self, config: EmptyConfig):
        super().__init__(config)
        self._config = config

    def build(self) -> Channel:
        return channel_utils.as_channel([])


class LocalFileBuilder(ConnectorBuilder):
    """LocalFileBuilder creates an instance of a LocalFile connector"""

    def __init__(self, config: LocalFileConfig):
        super().__init__(config)
        self._config = config

    def build(self) -> Channel:
        from os import path
        from tfx.utils.dsl_utils import external_input

        abspath = path.abspath(self._config.path)
        return external_input(abspath)


class Builder(ConnectorBuilder):
    def __init__(self, config: Optional[ConnectorConfig] = None):
        super().__init__(config)

        self._config = config or ConnectorConfig()
        self._connector_builders: Dict[Text, Type[ConnectorBuilder]] = {
            'empty': EmptyBuilder,
            'local_file': LocalFileBuilder,
        }

    def build(self) -> Channel:
        connector_name = self._config.WhichOneof('config')
        if connector_name in self._connector_builders:
            builder_constructor = self._connector_builders[connector_name]
            args = getattr(self._config, connector_name)
            builder = builder_constructor(args)
            return builder.build()
        else:
            raise ValueError(
                'Unknown connector name {0}'.format(connector_name))
