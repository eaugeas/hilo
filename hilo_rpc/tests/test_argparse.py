from argparse import ArgumentParser, Namespace
import unittest


from hilo_rpc.argparse import (
    add_props_to_parser,
    create_object_from_dict,
    fill_in_properties_from_args,
)

from hilo_rpc.proto.storage_pb2 import InputConfig


class ArgparseTest(unittest.TestCase):

    def test_add_props_to_parser_ok_source_config(self):
        parser = ArgumentParser()
        add_props_to_parser(InputConfig, parser)

        args = parser.parse_args([
            '-input_config.local_file.path', 'filepath'])

        self.assertEqual(
            getattr(args, 'input_config.local_file.path'),
            'filepath')

    def test_fill_in_properties_from_args_ok_source_config(self):
        args = Namespace(**{
            'input_config.local_file.path': 'filepath',
        })

        input_config: InputConfig = fill_in_properties_from_args(
            args, InputConfig)

        self.assertEqual(
            input_config.local_file.path,
            'filepath')

    def test_create_object_from_dict(self):
        input_config = create_object_from_dict(
            {'local_file': {'path': 'filepath'}},
            'hilo_rpc.proto.InputConfig')

        self.assertTrue(isinstance(input_config, InputConfig))
        self.assertEqual(
            input_config.local_file.path,
            'filepath')


if __name__ == '__main__':
    unittest.main()
