from typing import List, Text


def ensure_protobuf_loaded():
    """ensure_protobuf_loaded loads all the protobuf modules within
    this module if they have not been loaded yet"""
    import hilo_rpc.proto.logging_pb2  # noqa: F401
    import hilo_rpc.proto.metadata_pb2  # noqa: F401
    import hilo_rpc.proto.pipeline_pb2  # noqa: F401
    import hilo_rpc.proto.sink_pb2  # noqa: F401
    import hilo_rpc.proto.source_pb2  # noqa: F401
    import hilo_rpc.proto.stage_pb2  # noqa: F401
    import hilo_rpc.proto.connector_pb2  # noqa: F401


def filenames() -> List[Text]:
    """filenames returns a list of the filenames of the protobuf
    files that are used to generate the contents of this module"""
    return [
        'hilo_rpc/proto/logging.proto',
        'hilo_rpc/proto/metadata.proto',
        'hilo_rpc/proto/pipeline.proto',
        'hilo_rpc/proto/sink.proto',
        'hilo_rpc/proto/source.proto',
        'hilo_rpc/proto/stage.proto',
        'hilo_rpc/proto/connector.proto',
    ]
