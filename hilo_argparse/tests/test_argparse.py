from argparse import ArgumentParser, Namespace
import unittest


from hilo_argparse import add_props_to_parser, fill_in_properties_from_args
from hilo_rpc.proto.source_pb2 import SourceConfig


class ArgparseTest(unittest.TestCase):

    def test_add_props_to_parser_ok_source_config(self):
        parser = ArgumentParser()
        add_props_to_parser(SourceConfig, parser)

        args = parser.parse_args([
            '-source_config.file.path', 'filepath',
            '-source_config.file.parser.tsv.separator', 'separator'])

        self.assertEqual(
            getattr(args, 'source_config.file.path'),
            'filepath')
        self.assertEqual(
            getattr(args, 'source_config.file.parser.tsv.separator'),
            'separator')

    def test_fill_in_properties_from_args_ok_source_config(self):
        args = Namespace(**{
            'source_config.file.path': 'filepath',
            'source_config.file.parser.tsv.separator': 'separator',
        })

        source_config: SourceConfig = fill_in_properties_from_args(
            args, SourceConfig)

        self.assertEqual(
            source_config.file.path,
            'filepath')
        self.assertEqual(
            source_config.file.parser.tsv.separator,
            'separator')


if __name__ == '__main__':
    unittest.main()
