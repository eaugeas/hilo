import argparse
from typing import Text

from hilo_cmd.cmd.cmd import Cmd


class ApplyCmd(Cmd):
    """ApplyCmd applies the contents of a specification file to
    the system"""
    def __init__(self):
        super().__init__(name='apply')

    def description(self) -> Text:
        return 'applies the operation to the system'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '-file', type=str,
            help='path to file to apply')

    def exec(self, args: argparse.Namespace):
        if not args.file:
            self.print_help()
            return

        ApplyCmd.apply(args.file)

    @staticmethod
    def apply(file: Text):
        from tfx.orchestration.beam.beam_dag_runner import BeamDagRunner
        from hilo_rpc.serialize.yaml import deserialize_from_file
        from hilo_stage.pipeline.builder import Builder, Pipeline

        pipeline = deserialize_from_file(file, Pipeline)
        BeamDagRunner().run(Builder(pipeline).build())