from typing import Dict, List, Optional, Text, Type

from google.protobuf.message import Message
from google.protobuf.symbol_database import SymbolDatabase
from google.protobuf import symbol_database as symbol_database_module

from hilo_rpc.proto import ensure_protobuf_loaded


class SymbolLoader(object):
    def load(self, url: Text) -> Type[Message]:
        raise NotImplementedError()

    def load_all(self, url: Text) -> Dict[Text, Message]:
        raise NotImplementedError()


class ProtobufSymbolLoader(SymbolLoader):
    """ProtobufSymbolLoader loads protobuf messages from the provided
    databases."""
    def __init__(
            self,
            symbol_databases: Optional[List[SymbolDatabase]] = None,
    ):
        super().__init__()
        self._symbol_databases: List[SymbolDatabase] = []
        if symbol_databases:
            for symbol_database in symbol_databases:
                self._symbol_databases.append(symbol_database)

        if len(self._symbol_databases) == 0:
            default_symbol_databases = ProtobufSymbolLoader._load_default()
            for symbol_database in default_symbol_databases:
                self._symbol_databases.append(symbol_database)

        if len(self._symbol_databases) == 0:
            raise RuntimeError(
                'Cannot start ProtobufSymbolLoader, no'
                ' instances of SymbolDatabase found')

        ensure_protobuf_loaded()

    def load(self, url: Text) -> Type[Message]:
        for symbol_database in self._symbol_databases:
            return symbol_database.GetSymbol(url)

    def load_all(self, url: Text) -> Dict[Text, Message]:
        messages: Dict[str, Message] = {}
        for symbol_database in self._symbol_databases:
            try:
                symbol_database_messages = symbol_database.GetMessages(url)
                for message in symbol_database_messages:
                    messages[message] = symbol_database_messages[message]
            except KeyError:
                pass
        return messages

    @staticmethod
    def _load_default() -> List[SymbolDatabase]:
        return [symbol_database_module.Default()]
