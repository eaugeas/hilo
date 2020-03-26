import logging
from typing import Dict, Any, Union

from hilo_rpc.proto.logging_pb2 import LoggingConfig


def basic_config(config: LoggingConfig):
    d: Dict[str, Union[int, Any]] = {}

    if config.level == 'INFO':
        d['level'] = logging.INFO
    elif config.level == 'DEBUG':
        d['level'] = logging.DEBUG
    elif not config.level:
        d['level'] = logging.INFO
    else:
        raise ValueError('Unknown logging level {0}'.format(d['level']))

    if config.filename:
        d['filename'] = config.filename

    logging.basicConfig(**d)  # type: ignore
