from argparse import ArgumentParser, Namespace
from functools import reduce
from typing import Any, Dict, List, Optional, Text, Type, Union
import yaml

from google.protobuf.message import Message
from google.protobuf.descriptor import Descriptor

from hilo_rpc.argparse.symbol_loader import ProtobufSymbolLoader


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


def _fill_in_keys_from_args(
        args: Dict[str, Any],
        message: Type[Message],
) -> List[Message]:

    descriptor = message.DESCRIPTOR
    if len(descriptor.fields) != 2:
        raise TypeError(
            'Expected *Entry protobuf type,'
            ' but instead got {0}'.format(descriptor))
    if descriptor.fields[0].name != 'key':
        raise TypeError(
            'Protobuf Map generates an *Entry'
            ' protobuf type that should have a `key` property')
    if descriptor.fields[1].name != 'value':
        raise TypeError(
            'Protobuf Map generates an *Entry'
            ' protobuf type that should have a `value` property')

    result = {}
    for key in args:
        result[str(key)] = str(args[key])

    return result


def _is_proto_map(message: Type[Message]) -> bool:
    descriptor = message.DESCRIPTOR
    return (len(descriptor.fields) == 2 and
            descriptor.fields[0].name == 'key' and
            descriptor.fields[1].name == 'value')


def _fill_in_properties_for_struct(
        args: Dict[str, Any],
        message: Type[Message],
        loader: ProtobufSymbolLoader
) -> Message:
    if _is_proto_map(message):
        return _fill_in_keys_from_args(args, message)
    else:
        return _fill_in_properties_from_args(
            args, message, loader)


def _fill_in_properties_for_list(
        args: Dict[str, Any],
        message: Type[Message],
        loader: ProtobufSymbolLoader
) -> List[Message]:
    result = []
    for el in args:
        record = _fill_in_properties_from_args(el, message, loader)
        result.append(record)
    return result


def _fill_in_properties_from_args(
        args: Dict[str, Any],
        message: Type[Message],
        loader: ProtobufSymbolLoader
) -> Message:
    descriptor = message.DESCRIPTOR
    props: Dict[str, Union[Message, Any]] = {}
    for field in descriptor.fields:
        if field.type == 11:
            field_message = loader.load(
                field.message_type.full_name)
            if field.name in args:
                if isinstance(args[field.name], dict):
                    props[field.name] = _fill_in_properties_for_struct(
                        args[field.name], field_message, loader)
                elif isinstance(args[field.name], list):
                    props[field.name] = _fill_in_properties_for_list(
                        args[field.name], field_message, loader)
                else:
                    raise TypeError(
                        'Protobuf fields of type 11 can only be '
                        'serialized as lists or dicts. Received '
                        '{0}.'.format(args[field.name]))
        elif 10 >= field.type >= 1 or field.type == 13:
            if field.name in args:
                props[field.name] = args[field.name]
        else:
            print('field: ', field, field.name)
            raise TypeError('Unknown field type {0}'.format(field.type))
    return message(**props)


def _get_symbol_loader(
        loader_opt: Optional[ProtobufSymbolLoader] = None
) -> ProtobufSymbolLoader:
    if loader_opt:
        loader: ProtobufSymbolLoader = loader_opt
        return loader
    else:
        return ProtobufSymbolLoader()


def fill_in_properties_from_yaml(
        filepath: Text,
        message: Type[Message],
        loader_opt: Optional[ProtobufSymbolLoader] = None
) -> Message:
    """Fills the properties in the provided message with the values
    found in a yaml file
    """
    with open(filepath) as f:
        args = yaml.load(f, Loader=yaml.SafeLoader)

    return fill_in_properties_from_dict(args, message, loader_opt)


def create_object_from_dict(
        args: Dict[str, Any],
        url: Text,
        loader_opt: Optional[ProtobufSymbolLoader] = None
) -> Message:
    loader = _get_symbol_loader(loader_opt)
    message = loader.load(url)
    return fill_in_properties_from_dict(args, message, loader)


def fill_in_properties_from_dict(
        args: Dict[str, Any],
        message: Type[Message],
        loader_opt: Optional[ProtobufSymbolLoader] = None
) -> Message:
    """Fills the properties in the provided message with the values
    found in a dict
    """
    loader = _get_symbol_loader(loader_opt)
    return _fill_in_properties_from_args(
        args, message, loader)


def _break_into_dicts(args: Namespace) -> Dict[str, Any]:
    """_break_into_dicts receives a namespace, which contains
    entries such as key1.key2.key3: value
    and creates a multi-level dictionary such as
    {key1: {key2: {key3: value}}}
    """
    d = vars(args)
    result = {}
    for flattened_key in d:
        split = flattened_key.split('.')
        it_result = result
        for key in split[:len(split) - 1]:
            if key not in it_result:
                it_result[key] = {}
            it_result = it_result[key]
        it_result[split[len(split)-1]] = d[flattened_key]
    return result


def fill_in_properties_from_args(
        args: Namespace,
        message: Type[Message],
        loader_opt: Optional[ProtobufSymbolLoader] = None,
) -> Message:
    """Fills the properties in the provided message with the values
    found in args
    """
    d = _break_into_dicts(args)
    descriptor = message.DESCRIPTOR
    key = camel_case_to_snake_case(descriptor.name)
    if key in d:
        d = d[key]
        if not isinstance(d, dict):
            raise ValueError(
                'Attempt to fill in properties of non '
                'dictionary type. Key {0}, values {1}.'.format(key, d))
    else:
        d: Dict[str, Any] = {}

    return fill_in_properties_from_dict(
        d, message, loader_opt)
