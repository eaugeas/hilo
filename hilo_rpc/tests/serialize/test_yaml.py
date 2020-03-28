import unittest

import io


from hilo_rpc.serialize.yaml import (
    serialize, deserialize)

from hilo_rpc.proto.storage_pb2 import (
    InputConfig, LocalFileConfig)


class SerializeTest(unittest.TestCase):

    def test_serialize_ok_input_config(self):
        stream = io.StringIO()
        message = InputConfig(local_file=LocalFileConfig(path='filepath'))

        serialize(stream, message)

        stream.seek(0)
        self.assertEqual(stream.read(-1), """empty:
  empty: false
local_file:
  path: filepath
""")

    def test_deserialize_ok_input_config(self):
        stream = io.StringIO(initial_value="""empty:
  empty: false
local_file:
  path: filepath
""")

        message = deserialize(stream, InputConfig)

        stream.seek(0)
        self.assertEqual(
            message,
            InputConfig(local_file=LocalFileConfig(path='filepath')))


if __name__ == '__main__':
    unittest.main()
