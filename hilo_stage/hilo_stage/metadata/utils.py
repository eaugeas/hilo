from hilo_rpc.proto.metadata_pb2 import MetadataStoreConfig


def is_metadata_store_defined(config: MetadataStoreConfig) -> bool:
    return config.WhichOneof('config') is not None
