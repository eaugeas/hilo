from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner

from hilo_rpc.serialize.argparse import (
    add_to_parser,
    deserialize_from_namespace,
)
from hilo_rpc.serialize.yaml import deserialize_from_file

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
    add_to_parser(parser, LoggingConfig)
    args = parser.parse_args(argv[1:])
    logging_config = deserialize_from_namespace(
        args, LoggingConfig)
    config_logging(logging_config)

    pipeline_descriptor = deserialize_from_file(
        args.path, PipelineDescriptor)

    pipeline = Pipeline(pipeline_descriptor)
    BeamDagRunner().run(pipeline.build())
