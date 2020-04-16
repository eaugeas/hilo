from typing import Any, Dict, Optional, Text, Type

from ml_metadata.proto.metadata_store_pb2 import ConnectionConfig

from hilo_stage.metadata.config import MetadataStoreConfig, SqliteConfig


class StoreBuilder(object):
    def __init__(self, any: Any):
        pass

    def build(self) -> ConnectionConfig:
        raise NotImplementedError()


class SQLiteBuilder(StoreBuilder):
    def __init__(self, config: SqliteConfig):
        super().__init__(config)
        self._config = config

    def build(self) -> ConnectionConfig:
        from tfx.orchestration import metadata

        return metadata.sqlite_metadata_connection_config(self._config.path)


class MetadataStoreBuilder(StoreBuilder):
    def __init__(self, config: Optional[MetadataStoreConfig] = None):
        super().__init__(config)

        self._config = config or MetadataStoreConfig()
        self._store_builders: Dict[Text, Type[StoreBuilder]] = {
            'sqlite': SQLiteBuilder,
        }

    def build(self) -> ConnectionConfig:
        store_name = self._config.WhichOneof('config')
        if store_name in self._store_builders:
            builder_constructor = self._store_builders[store_name]
            args = getattr(self._config, store_name)
            builder = builder_constructor(args)
            return builder.build()
        else:
            raise ValueError('Unknown store name {0}'.format(store_name))
