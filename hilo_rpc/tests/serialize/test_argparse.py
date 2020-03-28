import unittest

from argparse import ArgumentParser, Namespace


from hilo_rpc.serialize.argparse import (
    add_to_parser,
    deserialize_from_namespace)

from hilo_rpc.proto.storage_pb2 import InputConfig


class SerializeTest(unittest.TestCase):

    def test_add_props_to_parser_ok_input_config(self):
        parser = ArgumentParser()
        add_to_parser(parser, InputConfig)

        args = parser.parse_args([
            '-input_config.local_file.path', 'filepath'])

        self.assertEqual(
            getattr(args, 'input_config.local_file.path'),
            'filepath')

    def test_fill_in_properties_from_args_ok_input_config(self):
        args = Namespace(**{
            'input_config.local_file.path': 'filepath',
        })

        input_config: InputConfig = deserialize_from_namespace(
            args, InputConfig)

        self.assertEqual(
            input_config.local_file.path,
            'filepath')


if __name__ == '__main__':
    unittest.main()
