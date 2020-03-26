from ml_metadata.proto.metadata_store_pb2 import ConnectionConfig
from tfx.orchestration import metadata

from hilo_stage.metadata.store import Store
from hilo_stage.metadata.config import (SqliteConfig, MetadataStoreConfig)


class SQLiteStore(Store):
    def __init__(self, config: SqliteConfig):
        super().__init__(config=MetadataStoreConfig(sqlite=config))
        self._config = config

    def connection_config(self) -> ConnectionConfig:
        return metadata.sqlite_metadata_connection_config(self._config.path)
