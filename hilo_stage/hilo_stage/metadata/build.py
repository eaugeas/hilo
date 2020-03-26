from hilo_stage.metadata.config import MetadataStoreConfig
from hilo_stage.metadata.store import Store
from hilo_stage.metadata.sqlite import SQLiteStore


def metadata_store_from_config(config: MetadataStoreConfig) -> Store:
    """Creates a new instance of a metadata store based on
    the provided configuration."""
    if config.WhichOneof('config') == 'sqlite':
        return SQLiteStore(config.sqlite)
    else:
        raise ValueError(
            'Unknown metadata store config value {0}'.format(
                config.WhichOneof('config')))