from io import IOBase
from typing import Text, Type, Union

from google.protobuf.message import Message
from google.protobuf import text_format

from hilo_rpc.serialize.size import MB


def _set_defaults(message: Message):
    for field in message.DESCRIPTOR.fields:
        value = getattr(message, field.name)
        if isinstance(value, int):
            setattr(message, field.name, 1)
        elif isinstance(value, float):
            setattr(message, field.name, 1.0)
        elif isinstance(value, str):
            setattr(message, field.name, field.name)
        elif isinstance(value, Message):
            _set_defaults(value)

        # TODO(): set defaults for all types. Maps, lists and
        # oneofs are missing


def deserialize(
        stream: IOBase,
        message: Union[Type[Message], Message],
        max_size: int = MB,
) -> Message:
    if isinstance(message, Type):
        message: Message = message()

    contents = stream.read(max_size + 1)
    if len(contents) > max_size:
        raise BufferError(
            'Message content length is greater than max_size')

    text_format.Parse(contents, message)
    return message


def deserialize_from_file(
        path: Text,
        message: Union[Type[Message], Message],
        max_size: int = MB,
) -> Message:
    with open(path, 'r') as f:
        return deserialize(f, message, max_size)


def serialize(
        stream: IOBase,
        message: Union[Type[Message], Message],
        set_defaults: bool = False,
):
    if isinstance(message, Message):
        message: Message = message
    else:
        message = message()
        if set_defaults:
            _set_defaults(message)
    text_format.PrintMessage(message, stream)


def serialize_to_file(
        path: Text,
        message: Union[Type[Message], Message],
        set_defaults: bool = False,
):
    with open(path, 'w') as f:
        serialize(
            f, message, set_defaults=set_defaults)
