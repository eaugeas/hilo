import io
from typing import Dict, Optional, Text, Type, Union

from google.protobuf.message import Message
import json

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
    """deserialize the contents of the json file to an instance
    of the provided message type"""
    args = json.load(stream)
    execute_directives(args)
    return deserialize_dict(args, message, symbol_loader)


def deserialize_from_file(
        filepath: Text,
        message: Type[Message],
        symbol_loader: Optional[SymbolLoader] = None,
        env: Optional[Dict[Text, Text]] = None,
        use_os_env: bool = False,
):
    """deserialize the contents of the yaml file to an instance
    of the provided message type"""
    with open(filepath) as f:
        return deserialize(f, message, symbol_loader)


def serialize(
        stream: io.IOBase,
        message: Union[Type[Message], Message],
        pretty: bool = False,
        with_types: bool = False
):
    """serialize serializes the message as yaml and writes the result
    to the stream"""
    serialized = serialize_dict(message, with_types=with_types)

    if pretty:
        json.dump(serialized, stream, indent=' ')
    else:
        json.dump(serialized, stream)


def serialize_file(
        filepath: Text,
        message: Type[Message],
        pretty: bool = False,
        with_types: bool = False
):
    """serialize_file serializes a message as a yaml into a file"""
    with open(filepath, 'w') as f:
        serialize(f, message, pretty=pretty, with_types=with_types)
