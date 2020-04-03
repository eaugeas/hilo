import io
from typing import Text, Type, Union

from google.protobuf.message import Message

from hilo_rpc.serialize.size import MB


def serialize_to_file(
        path: Text,
        message: Message
):
    with open(path, 'wb') as f:
        serialize(f, message)


def serialize(
        stream: io.RawIOBase,
        message: Message
):
    stream.write(message.SerializeToString())


def deserialize(
        stream: io.RawIOBase,
        message: Union[Type[Message], Message],
        max_size: int = MB,
) -> Message:
    if isinstance(message, Message):
        record: Message = message
    else:
        record = message()

    contents = stream.read(max_size + 1)
    if len(contents) > max_size:
        raise BufferError(
            'Message content length is greater than max_size')
    record.ParseFromString(contents)
    return record


def deserialize_from_file(
        path: Text,
        message: Message,
        max_size: int = MB,
):
    with open(path, 'rb') as f:
        deserialize(f, message, max_size)
