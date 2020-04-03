import unittest

import io

from hilo_rpc.serialize.json import serialize, deserialize
from hilo_rpc.proto.tests_pb2 import TestMessage


class SerializeTest(unittest.TestCase):

    def test_serialize_ok_input_config(self):
        stream = io.StringIO()
        message = TestMessage(
            enum=TestMessage.Enum(bool_enum=True),
            params=TestMessage.Params(
                bool_param=True,
                int32_param=1,
                string_param='hello'
            )
        )

        serialize(stream, message)

        stream.seek(0)
        self.assertEqual(
            '{"enum": {"bool_enum": true, "int32_enum": 0,'
            ' "string_enum": ""}, "params": {"bool_param": true, '
            '"int32_param": 1, "string_param": "hello"}, "mapping": {},'
            ' "string_repeated": []}', stream.read(-1))

    def test_serialize_ok_pretty_print(self):
        stream = io.StringIO()
        message = TestMessage(
            enum=TestMessage.Enum(bool_enum=True),
            params=TestMessage.Params(
                bool_param=True,
                int32_param=1,
                string_param='hello'
            )
        )

        serialize(stream, message, pretty=True)

        stream.seek(0)
        self.assertEqual("""{
 "enum": {
  "bool_enum": true,
  "int32_enum": 0,
  "string_enum": ""
 },
 "params": {
  "bool_param": true,
  "int32_param": 1,
  "string_param": "hello"
 },
 "mapping": {},
 "string_repeated": []
}""", stream.read(-1))

    def test_deserialize_ok_input_config(self):
        s = ('{"enum": '
             '{"bool_enum": true}, "params": {"bool_param": true, '
             '"int32_param": 1, "string_param": "hello"}, "mapping": {},'
             ' "string_repeated": []}')
        stream = io.StringIO(initial_value=s)

        message = deserialize(stream, TestMessage)

        self.assertEqual(TestMessage(
                enum=TestMessage.Enum(bool_enum=True),
                params=TestMessage.Params(
                    bool_param=True,
                    int32_param=1,
                    string_param='hello'
                )
            ), message)


if __name__ == '__main__':
    unittest.main()
