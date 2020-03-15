from argparse import ArgumentParser, Namespace
from functools import reduce
from typing import Any, Dict, Optional, Text, Type, Union

from google.protobuf.message import Message
from google.protobuf.descriptor import Descriptor
from google.protobuf import symbol_database as symbol_database_module
from google.protobuf.symbol_database import SymbolDatabase


def camel_case_to_snake_case(s: Text) -> Text:
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, s).lower()


def no_filter(prop: Text) -> bool:
    return True


def hidden_filter(prop: Text) -> bool:
    return not prop and prop[0] != '_'


def _augment_namespace(current: Text, additional: Text) -> Text:
    if current:
        return '{0}.{1}'.format(current, additional)
    else:
        return additional


def _add_props_to_parser(
        namespace: Text,
        descriptor: Descriptor,
        parser: ArgumentParser,
        prop_filter=no_filter):

    for field in descriptor.fields:
        field_namespace = _augment_namespace(namespace, field.name)
        if field.type == 9:
            parser.add_argument('-{0}'.format(field_namespace), type=str)
        elif field.type == 8:
            parser.add_argument('-{0}'.format(field_namespace), type=bool)
        elif field.type == 11:
            _add_props_to_parser(
                field_namespace,
                field.message_type,
                parser,
                prop_filter=prop_filter)


def add_props_to_parser(
        message: Type[Message],
        parser: ArgumentParser,
        prop_filter=no_filter):
    """
    Adds all the properties of the message as command
    line options to be parsed by the parser
    """
    descriptor = message.DESCRIPTOR
    namespace = camel_case_to_snake_case(descriptor.name)
    _add_props_to_parser(
        namespace, descriptor,
        parser, prop_filter=prop_filter)


def _fill_in_properties_from_args(
        namespace: Text,
        args: Dict[str, Any],
        message: Type[Message],
        symbol_database: SymbolDatabase) -> Message:
    descriptor = message.DESCRIPTOR
    props: Dict[str, Union[Message, Any]] = {}
    for field in descriptor.fields:
        field_namespace = _augment_namespace(namespace, field.name)
        if field.type == 11:
            field_message = symbol_database.GetSymbol(
                field.message_type.full_name)
            props[field.name] = _fill_in_properties_from_args(
                field_namespace, args, field_message, symbol_database)
        else:
            if field_namespace in args:
                props[field.name] = args[field_namespace]

    return message(**props)


def fill_in_properties_from_args(
        args: Namespace,
        message: Type[Message],
        symbol_database_opt: Optional[SymbolDatabase] = None) -> Message:
    """
    Fills the properties in the provided message with the values
    found in args
    """
    if symbol_database_opt:
        symbol_database: SymbolDatabase = symbol_database_opt
    else:
        symbol_database = symbol_database_module.Default()

    descriptor = message.DESCRIPTOR
    namespace = camel_case_to_snake_case(descriptor.name)
    return _fill_in_properties_from_args(
        namespace, vars(args), message, symbol_database)
