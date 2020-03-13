from typing import Optional, Text

from hilo_rpc.proto.source_pb2 import SourceConfig
from hilo_rpc.argparse import (
    add_props_to_parser,
    fill_in_properties_from_args)

from hilo_tool_src.pipeline.pipeline_builder import PipelineBuilder
from hilo_tool_src.pipeline.ingest_pipeline import IngestPipelineBuilder


def get_pipeline_builder(pipeline_name: Optional[Text]) -> PipelineBuilder:
    if pipeline_name == 'ingest':
        return IngestPipelineBuilder()
    elif not pipeline_name:
        raise ValueError('-pipeline option must be set')
    else:
        raise ValueError(
            'unknown value {0} for option -pipeline'.format(pipeline_name))


def main(argv):
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='command line utility to execute pipelines')
    parser.add_argument('-pipeline', type=str, help=(
        'name of the pipeline to execute'))
    add_props_to_parser(
        SourceConfig, parser)
    args = parser.parse_args(argv[1:])
    source_config = fill_in_properties_from_args(
        args, SourceConfig)

    print('config: ', source_config)
    try:
        builder = get_pipeline_builder(args.pipeline)
    except ValueError as e:
        print(str(e))
        parser.print_help()
        sys.exit(1)

    pipeline = builder.build()
    print(pipeline)
