from io import IOBase
from typing import Text, Type, Union

from google.protobuf.message import Message
from google.protobuf import text_format

from hilo_rpc.serialize.size import MB


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
        message: Message
):
    text_format.PrintMessage(message, stream)


def serialize_to_file(
        path: Text,
        message: Message
):
    with open(path, 'w') as f:
        serialize(f, message)
