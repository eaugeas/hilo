import argparse
from typing import List, Optional, Text


class Cmd(object):
    """Cmd provides an interface for command line commands"""
    def __init__(self, name: Text, subcommands: Optional[List['Cmd']] = None):
        self._name = name
        self._subcommands = subcommands

    def description(self) -> Text:
        return ''

    def name(self) -> Text:
        return self._name

    def bind_self(self, parser: argparse.ArgumentParser):
        fns = parser.get_default('fns')

        if self.exec not in fns:
            fns.append(self.exec)
            parser.set_defaults(fns=fns)

    def add_arguments(self, parser: argparse.ArgumentParser):
        if parser.get_default('exec') is None:
            parser.set_defaults(exec=Cmd.runner)
            parser.set_defaults(fns=[self.exec])
        else:
            self.bind_self(parser)

        fns = parser.get_default('fns')
        subparsers = parser.add_subparsers(title='commands')

        if self._subcommands is not None:
            for command in self._subcommands:
                subparser = subparsers.add_parser(command.name(),
                                                  help=command.description())
                command.add_arguments(subparser)
                current = [fn for fn in fns]
                current.append(command.exec)
                subparser.set_defaults(fns=current)

    @staticmethod
    def has_next(args: argparse.Namespace) -> bool:
        return len(args.fns) > 0

    @staticmethod
    def runner(args: argparse.Namespace):
        while len(args.fns) > 0:
            fn = args.fns.pop(0)
            fn(args)

    def print_help(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)
        parser.print_help()

    def exec(self, args: argparse.Namespace):
        if not Cmd.has_next(args):
            self.print_help()
