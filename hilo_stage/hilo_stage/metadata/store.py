from ml_metadata.proto.metadata_store_pb2 import ConnectionConfig

from hilo_stage.metadata.config import MetadataStoreConfig


class Store(object):
    def __init__(self, config: MetadataStoreConfig):
        self._config = config

    def config(self) -> MetadataStoreConfig:
        return self._config

    def connection_config(self) -> ConnectionConfig:
        raise NotImplementedError()
