import unittest
from argparse import ArgumentParser, Namespace

from hilo_rpc.proto.tests_pb2 import TestMessage
from hilo_rpc.serialize.argparse import (add_to_parser,
                                         deserialize_from_namespace)


class SerializeTest(unittest.TestCase):
    def test_add_props_to_parser_ok_input_config(self):
        parser = ArgumentParser()
        add_to_parser(parser, TestMessage)

        args = parser.parse_args([
            '-test_message.enum.int32_enum', '1',
            '-test_message.params.bool_param', 'True',
            '-test_message.params.int32_param', '2',
            '-test_message.params.string_param', 'bye'
        ])

        self.assertEqual(getattr(args, 'test_message.enum.int32_enum'), '1')
        self.assertEqual(getattr(args, 'test_message.params.bool_param'),
                         'True')
        self.assertEqual(getattr(args, 'test_message.params.int32_param'), '2')
        self.assertEqual(getattr(args, 'test_message.params.string_param'),
                         'bye')

    def test_fill_in_properties_from_args_ok_input_config(self):
        args = Namespace(
            **{
                'test_message.enum.int32_enum': '1',
                'test_message.params.bool_param': 'True',
                'test_message.params.int32_param': '2',
                'test_message.params.string_param': 'bye'
            })

        message: TestMessage = deserialize_from_namespace(args, TestMessage)

        self.assertEqual(message.enum.int32_enum, 1)
        self.assertEqual(message.params.bool_param, True)
        self.assertEqual(message.params.int32_param, 2)
        self.assertEqual(message.params.string_param, 'bye')


if __name__ == '__main__':
    unittest.main()
