from hilo_rpc.proto.source_pb2 import SourceConfig
import hilo_argparse


def main(argv):
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='command line utility to execute pipelines')
    parser.add_argument('-pipeline', type=str, help=(
        'name of the pipeline to execute'))
    hilo_argparse.add_props_to_parser(
        SourceConfig, parser,
        prop_filter=hilo_argparse.hidden_filter)
    args = parser.parse_args(argv[1:])

    source_config = hilo_argparse.fill_in_properties_from_args(
        args, SourceConfig)

    if not args.pipeline:
        print('ERROR: -pipeline option must be set')
        print()
        parser.print_help()
        sys.exit(0)

    print(source_config)
