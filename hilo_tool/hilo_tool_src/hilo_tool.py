from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

from hilo_rpc.argparse import (
    add_props_to_parser,
    fill_in_properties_from_args,
    fill_in_properties_from_yaml
)

from hilo_tool_src.logging.config import (
    LoggingConfig, basic_config as config_logging)
from hilo_stage.pipeline.pipeline import Pipeline, PipelineDescriptor


def main(argv):
    import argparse

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

    pipeline = Pipeline(pipeline_descriptor)
    BeamDagRunner().run(pipeline.build())
