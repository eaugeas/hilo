from hilo_stage.storage.config import InputConfig
from hilo_stage.storage.input import Input
from hilo_stage.storage.empty import Empty
from hilo_stage.storage.local_file import LocalFile


def input_from_config(config: InputConfig) -> Input:
    """input_from_config creates a new instance of an Input
    from the provided configuration"""
    if config.WhichOneof('config') == 'empty':
        return Empty(config.empty)
    elif config.WhichOneof('config') == 'local_file':
        return LocalFile.from_config(config.local_file)
    else:
        raise ValueError(
            'Unknown input config value {0}'.format(
                config.WhichOneof('config')))
