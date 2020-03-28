from functools import reduce
from typing import Any, Dict, List, Optional, Text, Type, Union

from google.protobuf.message import Message
from google.protobuf.descriptor import Descriptor
from google.protobuf.pyext._message import (
    ScalarMapContainer, MessageMapContainer,
    RepeatedScalarContainer, RepeatedCompositeContainer)

from hilo_rpc.serialize.symbol_loader import (
    SymbolLoader, ProtobufSymbolLoader)


def camel_case_to_snake_case(s: Text) -> Text:
    """camel_case_to_snake_case converts the formatting in
    s from camelCase to snake_case"""
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, s).lower()


def _namespace(
        current: Text,
        addition: Text,
        sep: Text = '.'
) -> Text:
    if current:
        return sep.join([current, addition])
    else:
        return addition


def _flatten_dict_rec(
        namespace: Text,
        d: Dict[str, Any],
        result: Dict[str, Any]
):
    for key in d:
        key_namespace = _namespace(namespace, key)
        if isinstance(d[key], int):
            result[key_namespace] = d[key]
        elif isinstance(d[key], float):
            result[key_namespace] = d[key]
        elif isinstance(d[key], str):
            result[key_namespace] = d[key]
        elif isinstance(d[key], dict):
            _flatten_dict_rec(key_namespace, d[key], result)
        elif isinstance(d[key], list):
            for i in range(0, len(d[key])):
                el_namespace = _namespace(key_namespace, i)
                _flatten_dict_rec(el_namespace, d[key][i], result)
        else:
            raise ValueError('Unexpected type for value {0}'.format(d[key]))


def flatten(d: Dict[str, Any], namespace: Text = '') -> Dict[str, Any]:
    """flatten flattens a multi-level dictionary into a single level
    dictionary.

    For example:
        d = {'key1': {'key2': 'value1'}}
     would be serialized into
        d = {'key1.key2': 'value1'}

    The input dictionary's values are expected to be simple values
    such as int, float, str, or other dictionaries or lists
    """
    result: Dict[str, Any] = {}
    _flatten_dict_rec(namespace, d, result)
    return result


def unflatten(d: Dict[str, Any], namespace: Text = '') -> Dict[str, Any]:
    """unflatten is the opposite operation of flatten_dict. It takes
    a single level dictionary and unflattens it to a multi level dictionary.

    For example:
        d = {'key1.key2': 'value1'}
     would be unflattened  into
        d = {'key1': {'key2': 'value1'}}
    """
    result = {}

    for key in d:
        newkey = key
        if namespace:
            newkey = key.lstrip('{0}.'.format(namespace))

        if isinstance(d[key], dict):
            raise ValueError(
                'unflatten_dict expects a '
                'single level dictionary. Received {0}'.format(d))
        split = newkey.split('.')
        it_result = result
        for level in split[:-1]:
            if level not in it_result:
                it_result[level] = {}
                it_result = it_result[level]
        it_result[split[-1]] = d[key]

    return result


def serialize(
        message: Union[Type[Message], Message],
        symbol_loader: Optional[SymbolLoader] = None,
        with_types: bool = False,
) -> Dict[str, Any]:
    """serialize_to_dict serializes the message type
    into a dictionary."""
    if not symbol_loader:
        symbol_loader: SymbolLoader = ProtobufSymbolLoader()

    result = {}

    def _get_value_from_simple_type(
            value: Any,
    ):
        if with_types:
            if isinstance(value, bool):
                return 'bool'
            elif isinstance(value, int):
                return 'int'
            elif isinstance(value, float):
                return 'float'
            elif isinstance(value, str):
                return 'Text'
        return value

    def _get_value_from_repeated(
            descriptor: Optional[Descriptor],
            value: Union[RepeatedScalarContainer, RepeatedCompositeContainer]
    ) -> List[Any]:
        repeated: List[Any] = []

        if len(value) == 0 and with_types:
            if isinstance(value, RepeatedCompositeContainer):
                repeated.append(serialize(
                    symbol_loader.load(descriptor.full_name),
                    with_types=with_types,
                    symbol_loader=symbol_loader))
            else:
                try:
                    value.append(True)
                    return ['bool']
                except TypeError:
                    pass
                try:
                    value.append(1)
                    return ['int']
                except TypeError:
                    pass
                try:
                    value.append(1.1)
                    return ['float']
                except TypeError:
                    pass
                try:
                    value.append('str')
                    return ['str']
                except TypeError:
                    pass
        else:
            for el in value:
                repeated.append(serialize(
                    el, with_types=with_types, symbol_loader=symbol_loader))
        return repeated

    def _get_value_from_map(
            descriptor: Optional[Descriptor],
            value: Union[ScalarMapContainer, MessageMapContainer]
    ) -> Dict[str, Any]:
        map = {}

        if len(value) == 0 and with_types:
            # TODO(): implement for maps
            pass
        else:
            for el in value:
                map[el.key] = serialize(
                    el.value,
                    with_types=with_types,
                    symbol_loader=symbol_loader)
        return map

    if _is_protobuf_message_type(message):
        record: Message = message()
    elif _is_protobuf_message(message):
        record: Message = message
    else:
        raise ValueError(
            'serialize expects a Union[Type[Message], Message]. '
            'Received {0}'.format(message))

    descriptor = record.DESCRIPTOR

    for field in descriptor.fields:
        value = getattr(record, field.name)
        if _is_protobuf_map(value):
            result[field.name] = _get_value_from_map(
                field.message_type, value)
        elif _is_protobuf_repeated(value):
            result[field.name] = _get_value_from_repeated(
                field.message_type, value)
        elif _is_protobuf_message(value):
            result[field.name] = serialize(
                value, with_types=with_types, symbol_loader=symbol_loader)
        else:
            result[field.name] = _get_value_from_simple_type(value)

    return result


def _is_protobuf_map(o: Any) -> bool:
    return (isinstance(o, ScalarMapContainer) or
            isinstance(o, MessageMapContainer))


def _is_protobuf_repeated(o: Any) -> bool:
    return (isinstance(o, RepeatedScalarContainer) or
            isinstance(o, RepeatedCompositeContainer))


def _is_protobuf_message_type(o: Any) -> bool:
    return isinstance(o, Type) and _is_protobuf_message(o())


def _is_protobuf_message(o: Any) -> bool:
    return isinstance(o, Message)


def _deserialize_protobuf_map_from_dict_rec(
        d: Dict[Text, Any],
        descriptor: Descriptor,
        symbol_loader: SymbolLoader,
        result: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if result is None:
        result: Dict[str, Any] = {}
    for key in d:
        # TODO(): check result type so that d[key] is converted to the
        # correct type
        result[key] = str(d[key])
    return result


def _deserialize_from_dict_rec(
        d: Dict[Text, Any],
        record: Message,
        symbol_loader: SymbolLoader
) -> Message:
    descriptor = record.DESCRIPTOR
    for field in descriptor.fields:
        if field.name not in d:
            continue

        field_value = getattr(record, field.name)
        if _is_protobuf_map(field_value):
            _deserialize_protobuf_map_from_dict_rec(
                d, descriptor, symbol_loader, result=field_value)
        elif _is_protobuf_repeated(field_value):
            _deserialize_list_from_dict_rec(
                d[field.name],
                field.message_type,
                symbol_loader,
                result=getattr(record, field.name))
        elif _is_protobuf_message(field_value):
            _deserialize_from_dict_rec(
                d[field.name], field_value, symbol_loader)
        else:
            setattr(record, field.name, d[field.name])
    return record


def _get_symbol_loader(
        symbol_loader: Optional[SymbolLoader] = None,
) -> SymbolLoader:
    return symbol_loader or ProtobufSymbolLoader()


def _get_message_instance(
        message: Optional[Union[Type[Message], Message]] = None,
        url: Optional[Text] = None,
        symbol_loader: Optional[SymbolLoader] = None,
) -> Message:
    if message:
        if isinstance(message, Message):
            record: Message = message
        else:
            record: Message = message()
    elif url:
        record: Message = symbol_loader.load(url)
    else:
        raise ValueError('either `message` or `url` must be set')
    return record


def deserialize(
        d: Dict[Text, Any],
        message: Optional[Union[Type[Message], Message]] = None,
        symbol_loader: Optional[SymbolLoader] = None,
        url: Optional[Text] = None
) -> Message:
    """deserialize_from_dict deserializes the dictionary into an
    instance of the provided message type"""
    symbol_loader: SymbolLoader = _get_symbol_loader(symbol_loader)
    record = _get_message_instance(
        message=message, url=url, symbol_loader=symbol_loader)
    return _deserialize_from_dict_rec(d, record, symbol_loader)


def _deserialize_list_from_dict_rec(
        elements: List[Any],
        descriptor: Descriptor,
        symbol_loader: SymbolLoader,
        result: Optional[List[Message]] = None
) -> List[Any]:
    if result is None:
        result: List[Any] = result or []

    for el in elements:
        if (isinstance(el, str) or
                isinstance(el, int) or
                isinstance(el, float)):
            result.append(el)

        elif isinstance(el, list):
            # TODO(): implement sublist deserialization
            raise ValueError(
                'Attempt to deserialize list whose elements should not be '
                'lists. Received {0}'.format(el))
        else:
            message = symbol_loader.load(descriptor.full_name)
            result.append(
                _deserialize_from_dict_rec(el, message(), symbol_loader)
            )

    return result
