import argparse
from abc import ABC

from hilo_src.cmd.cmd import Cmd
from hilo_src.help.entity import (
    describe as describe_entity,
    find as find_entity)


class EntityHelpCmd(Cmd, ABC):
    """EntityHelpCmd provides documentation for all the entities
    defined in the Hilo APIs"""
    def __init__(self):
        super().__init__(name='entity')

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '-name', type=str,
            help='identifying name of the entity. If an entity is found '
                 'that matches the name, that will be displayed. '
                 'Otherwise, all entities that have a name that match '
                 'the name provided will be listed')
        parser.add_argument(
            '-formatter', type=str, default='yaml',
            help='output formatter used. Options are `yaml` and `json`'
        )

    def exec(self, args: argparse.Namespace):
        entities = find_entity(args.name)
        if len(entities) > 1:
            for entity in entities:
                print(entity.DESCRIPTOR.full_name)
        elif len(entities) == 1:
            print(describe_entity(entities[0], args.formatter))


class HelpCmd(Cmd, ABC):
    """HelpCmd implements the help command. It provides a means of
    self documentation for Hilo"""
    def __init__(self):
        super().__init__(name='help', subcommands=[EntityHelpCmd()])
