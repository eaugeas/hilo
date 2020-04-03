import argparse

from hilo_cmd.cmd.cmd import Cmd
from hilo_src.help.cmd import HelpCmd


class HiloCmd(Cmd):
    def __init__(self):
        super().__init__('hilo', subcommands=[HelpCmd()])


def main(argv):
    hilo = HiloCmd()
    parser = argparse.ArgumentParser()
    hilo.add_arguments(parser)
    args = parser.parse_args(argv)
    args.exec(args)
