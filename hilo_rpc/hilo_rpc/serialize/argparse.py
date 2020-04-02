from argparse import ArgumentParser, Namespace
from typing import Type

from google.protobuf.message import Message

from hilo_rpc.serialize.dict import (
    camel_case_to_snake_case,
    deserialize,
    flatten,
    unflatten,
    serialize)


def add_to_parser(
        parser: ArgumentParser,
        message: Type[Message],
):
    """add_to_parser adds all the properties in the provided
    type to the parser as CLI options"""
    descriptor = message.DESCRIPTOR
    namespace = camel_case_to_snake_case(descriptor.name)
    serialized = serialize(message)
    flattened = flatten(serialized, namespace=namespace)
    for key in flattened:
        parser.add_argument('-{0}'.format(key), required=False)


def deserialize_from_namespace(
        args: Namespace,
        message: Type[Message]
) -> Message:
    """deserialize_from_namespace deserializes an instance of
    the provided message type from the values in the namespace"""
    descriptor = message.DESCRIPTOR
    namespace = camel_case_to_snake_case(descriptor.name)
    d = unflatten(vars(args), namespace=namespace)
    return deserialize(d, message)
