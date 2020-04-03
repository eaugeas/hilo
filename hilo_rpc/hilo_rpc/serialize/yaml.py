import io
from typing import Optional, Text, Type, Union

from google.protobuf.message import Message
import yaml

from hilo_rpc.serialize.symbol_loader import SymbolLoader
from hilo_rpc.serialize.directive import execute as execute_directives
from hilo_rpc.serialize.dict import (
    deserialize as deserialize_dict,
    serialize as serialize_dict)


def deserialize(
        stream: io.IOBase,
        message: Type[Message],
        symbol_loader: Optional[SymbolLoader] = None,
):
    """deserialize the contents of the yaml file to an instance
    of the provided message type"""
    args = yaml.load(stream, Loader=yaml.SafeLoader)
    execute_directives(args)
    return deserialize_dict(args, message, symbol_loader)


def deserialize_from_file(
        filepath: Text,
        message: Type[Message],
        symbol_loader: Optional[SymbolLoader] = None
):
    """deserialize the contents of the yaml file to an instance
    of the provided message type"""
    with open(filepath) as f:
        return deserialize(f, message, symbol_loader)


def serialize(
        stream: io.IOBase,
        message: Union[Type[Message], Message],
        with_types: bool = False
):
    """serialize serializes the message as yaml and writes the result
    to the stream"""
    serialized = serialize_dict(message, with_types=with_types)
    yaml.dump(serialized, stream=stream)


def serialize_file(
        filepath: Text,
        message: Type[Message],
        with_types: bool = False
):
    """serialize_file serializes a message as a yaml into a file"""
    with open(filepath, 'w') as f:
        serialize(f, message, with_types=with_types)