import unittest

import io

from hilo_rpc.serialize.yaml import serialize, deserialize
from hilo_rpc.proto.tests_pb2 import TestMessage


class SerializeTest(unittest.TestCase):
    def test_serialize_ok_input_config(self):
        stream = io.StringIO()
        message = TestMessage(enum=TestMessage.Enum(bool_enum=True),
                              params=TestMessage.Params(bool_param=True,
                                                        int32_param=1,
                                                        string_param='hello'))

        serialize(stream, message)

        stream.seek(0)
        self.assertEqual(
            """enum:
  bool_enum: true
mapping: {}
params:
  bool_param: true
  int32_param: 1
  string_param: hello
params_map: {}
params_repeated: []
string_repeated: []
""", stream.read(-1))

    def test_deserialize_ok_input_config(self):
        stream = io.StringIO(initial_value="""enum:
  bool_enum: true
params:
  bool_param: true
  int32_param: 1
  string_param: hello
""")

        message = deserialize(stream, TestMessage)

        stream.seek(0)
        self.assertEqual(
            TestMessage(enum=TestMessage.Enum(bool_enum=True),
                        params=TestMessage.Params(bool_param=True,
                                                  int32_param=1,
                                                  string_param='hello')),
            message)


if __name__ == '__main__':
    unittest.main()
