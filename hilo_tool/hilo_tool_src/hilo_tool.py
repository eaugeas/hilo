from hilo_rpc.proto.source_pb2 import SourceConfig
from hilo_rpc.proto.pipeline_pb2 import PipelineConfig
from hilo_rpc.argparse import (
    add_props_to_parser,
    fill_in_properties_from_args)

from hilo_tool_src.pipeline.pipeline_builder import PipelineBuilder
from hilo_tool_src.pipeline.train_pipeline import TrainPipelineBuilder
from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner


def get_pipeline_builder(pipeline_config: PipelineConfig) -> PipelineBuilder:
    if pipeline_config.WhichOneof('pipeline') == 'train':
        return TrainPipelineBuilder(
            data_root=pipeline_config.train.data_root,
            metadata_path=pipeline_config.train.metadata_path,
            pipeline_name=pipeline_config.train.pipeline_name,
            pipeline_root=pipeline_config.train.pipeline_root,
            enable_cache=pipeline_config.train.enable_cache)
    elif pipeline_config.WhichOneof('pipeline') is None:
        raise ValueError('no pipeline set in configuration')
    else:
        raise ValueError(
            'unknown pipeline type set in configuration `{0}`'
            .format(pipeline_config.WhichOneof('pipeline')))


def main(argv):
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='command line utility to execute pipelines')
    add_props_to_parser(SourceConfig, parser)
    add_props_to_parser(PipelineConfig, parser)
    args = parser.parse_args(argv[1:])
    source_config = fill_in_properties_from_args(
        args, SourceConfig)
    pipeline_config = fill_in_properties_from_args(
        args, PipelineConfig)

    print('config: ', source_config)
    try:
        builder = get_pipeline_builder(pipeline_config)
    except ValueError as e:
        print(str(e))
        parser.print_help()
        sys.exit(1)

    pipeline = builder.build()
    BeamDagRunner().run(pipeline)
