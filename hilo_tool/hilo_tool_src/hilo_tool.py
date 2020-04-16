import argparse

from hilo_cmd.cmd.cmd import Cmd
from hilo_rpc.serialize.argparse import (
    add_to_parser,
    deserialize_from_namespace,
)
from hilo_tool_src.apply import ApplyCmd
from hilo_tool_src.example import ExampleCmd
from hilo_tool_src.logging.config import (LoggingConfig, basic_config as
                                          config_logging)


class HiloToolCmd(Cmd):
    def __init__(self):
        super().__init__('hilo_tool', subcommands=[ApplyCmd(), ExampleCmd()])

    def add_arguments(self, parser: argparse.ArgumentParser):
        add_to_parser(parser, LoggingConfig)
        super().add_arguments(parser)

    def exec(self, args: argparse.Namespace):
        logging_config = deserialize_from_namespace(args, LoggingConfig)
        config_logging(logging_config)

        if not Cmd.has_next(args):
            self.print_help()


def main(argv):
    hilo = HiloToolCmd()
    parser = argparse.ArgumentParser()
    hilo.add_arguments(parser)
    args = parser.parse_args(argv[1:])
    args.exec(args)
