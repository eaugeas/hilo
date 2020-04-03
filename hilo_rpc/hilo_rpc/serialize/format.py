import io
from typing import Any, Dict, List, Text, Type, Union

from google.protobuf.message import Message

from hilo_rpc.serialize import json, text, yaml


class Serializer(object):
    def __init__(
            self,
            fn: Any,
            args: List[Text],
    ):
        self._serialize = fn
        self._args = args

    def serialize(self, stream, message, **kwargs):
        props = {}

        for el in kwargs:
            if el in self._args:
                props[el] = kwargs[el]

        self._serialize(stream, message, **props)


def serialize(
    stream: io.IOBase,
    message: Union[Message, Type[Message]],
    **kwargs
):
    formatters: Dict[str, Serializer] = {
        'json': Serializer(json.serialize, ['pretty', 'with_types']),
        'text': Serializer(text.serialize, ['set_defaults']),
        'yaml': Serializer(yaml.serialize, ['with_types']),
    }

    if 'formatter' not in kwargs:
        kwargs['formatter'] = 'yaml'

    if kwargs['formatter'] in formatters:
        formatter = kwargs['formatter']
        formatters[formatter].serialize(
            stream,
            message,
            **kwargs)
    else:
        raise KeyError(
            'Unknown formatter {0}. Valid formatters are: {1}'.format(
                kwargs['formatter'], ', '.join(formatters.keys())))
