import argparse
from typing import List, Optional, Text


class Cmd(object):
    """Cmd provides an interface for command line commands"""
    def __init__(self, name: Text, subcommands: Optional[List['Cmd']] = None):
        self._name = name
        self._subcommands = subcommands

    def name(self) -> Text:
        return self._name

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.set_defaults(exec=self.exec)
        subparsers = parser.add_subparsers(title='commands')

        if self._subcommands is not None:
            for command in self._subcommands:
                subparser = subparsers.add_parser(command.name())
                command.add_arguments(subparser)
                subparser.set_defaults(exec=command.exec)

    def exec(self, args: argparse.Namespace):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)
        parser.print_help()
