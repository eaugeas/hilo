from hilo_rpc.proto.source_pb2 import SourceConfig
from hilo_stage.storage.config import (
    InputConfig, EmptyConfig, LocalFileConfig)


def source_config_from_input_config(
        config: InputConfig,
) -> SourceConfig:
    """"source_config_from_input_descriptor creates an instance of
    a SourceConfig from the provided input descriptor"""
    if isinstance(config, LocalFileConfig):
        return SourceConfig(file=config)
    elif isinstance(config, EmptyConfig):
        return SourceConfig(empty=config)
    else:
        raise ValueError('Unknown input descriptor instance {0}'.format(config))
