from typing import List, Optional, Text, Type, Union

from google.protobuf.message import Message

from hilo_rpc.proto import filenames as proto_filenames
from hilo_rpc.serialize.dict import serialize
from hilo_rpc.serialize.symbol_loader import ProtobufSymbolLoader


def find(name: Optional[Text]) -> List[Message]:
    """Finds all the entities that match the properties provided"""
    symbol_loader = ProtobufSymbolLoader()
    messages = symbol_loader.load_all(proto_filenames())

    if name and name in messages:
        return [messages[name]]

    result: List[Message] = list(map(
        lambda item: item[1],  # type: ignore
        filter(
            lambda el: name is None or el[0].find(name) != -1,
            messages.items()
        )
    ))
    return result


def describe(
        message: Union[Message, Type[Message]],
        formatter: Optional[Text] = 'yaml'
) -> Text:
    """Provides a full description of the entity based on the
    properties provided. If no empty is found, an error is raised"""

    import io
    import json
    import yaml

    serialized = serialize(message, with_types=True)
    if formatter == 'json':
        return json.dumps(serialized, indent='  ')
    elif formatter is None or formatter == 'yaml':
        s = io.StringIO()
        yaml.dump(serialized, s)
        s.seek(0)
        return s.read(-1)
    else:
        raise ValueError(
            'Unknown description format for entity {0}. '
            'Supported formats are: `json`.'.format(formatter))
