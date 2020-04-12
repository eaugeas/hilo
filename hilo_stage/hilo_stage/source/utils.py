from hilo_rpc.proto.source_pb2 import Source


def is_source_defined(source: Source) -> bool:
    return source.config.WhichOneof('config') is not None
