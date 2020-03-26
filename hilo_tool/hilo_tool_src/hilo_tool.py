from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
#
# from hilo_rpc.proto.source_pb2 import SourceConfig
# from hilo_rpc.proto.pipeline_pb2 import PipelineConfig
from hilo_rpc.argparse import (
    add_props_to_parser,
    fill_in_properties_from_args,
    fill_in_properties_from_yaml
)

from hilo_tool_src.logging.config import (
    LoggingConfig, basic_config as config_logging)
from hilo_stage.pipeline.pipeline import Pipeline, PipelineDescriptor
# from hilo_tool_src.pipeline.pipeline_builder import PipelineBuilder
# from hilo_tool_src.pipeline.train_pipeline import TrainPipelineBuilder


# def get_pipeline_builder(pipeline_config: PipelineConfig) -> PipelineBuilder:
#     if pipeline_config.WhichOneof('pipeline') == 'train':
#         return TrainPipelineBuilder(
#             data_root=pipeline_config.train.data_root,
#             metadata_path=pipeline_config.train.metadata_path,
#             pipeline_name=pipeline_config.train.pipeline_name,
#             pipeline_root=pipeline_config.train.pipeline_root,
#             enable_cache=pipeline_config.train.enable_cache)
#     elif pipeline_config.WhichOneof('pipeline') is None:
#         raise ValueError('no pipeline set in configuration')
#     else:
#         raise ValueError(
#             'unknown pipeline type set in configuration `{0}`'
#             .format(pipeline_config.WhichOneof('pipeline')))


def main(argv):
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='command line utility to execute pipelines')
    parser.add_argument(
        '-path', default=None, type=str,
        help='path to a yaml file that defines a pipeline')
    add_props_to_parser(LoggingConfig, parser)
    args = parser.parse_args(argv[1:])
    logging_config = fill_in_properties_from_args(
        args, LoggingConfig)
    config_logging(logging_config)

    pipeline_descriptor = fill_in_properties_from_yaml(
        args.path, PipelineDescriptor)
    print('logging_config: ', logging_config)
    print('pipeline: ', pipeline_descriptor)

    pipeline = Pipeline(pipeline_descriptor)
    BeamDagRunner().run(pipeline.build())
