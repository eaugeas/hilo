import argparse
from typing import Text

from hilo_cmd.cmd.cmd import Cmd
from hilo_tool_src.apply import ApplyCmd


class ExampleCmd(Cmd):
    """ExampleCmd executes examples. Examples are directories
    that follow a specific structure, and they are intended for
    showcase purposes. This command line tool's purpose is to aid
    in the execution of examples and make the process of executing
    examples as easy, straightforward, and self documented as
    possible"""

    def __init__(self):
        super().__init__(name='example')

    def description(self) -> Text:
        return (
            'manage the execution of examples. Examples are directories'
            'that follow a specific structure, that showcase some '
            ' functionality of hilo. The purpose of this command is to make '
            'the execution of examples easy.')

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '-path', type=str, help='path to example\'s root directory')

    def exec(self, args: argparse.Namespace):
        if not args.path:
            self.print_help()
            return

        ExampleCmd.apply(args.path)

    @staticmethod
    def apply(path: Text):
        import os

        path = os.path.abspath(path)
        if not os.path.isdir(path):
            raise ValueError(
                'Path {0} is not a directory. The path must be set to '
                'the root folder of the example.'.format(path))

        pipeline_file_path = os.path.join(path, 'pipeline.yaml')
        if not os.path.isfile(pipeline_file_path):
            raise ValueError(
                'An example must contain a pipeline.yaml file. The path '
                'provided, {0}, does not contain a pipeline.yaml'
                ' file.'.format(path))

        # examples must use EXAMPLE_ROOT as environment variable
        # to define their project root
        os.environ['EXAMPLE_ROOT'] = path
        ApplyCmd.apply(pipeline_file_path)
