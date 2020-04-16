import unittest

import io

from hilo_rpc.proto.tests_pb2 import TestMessage
from hilo_rpc.serialize.proto import deserialize, serialize


class ProtoTest(unittest.TestCase):
    def test_serialize_ok(self):
        stream = io.BytesIO()
        message = TestMessage(enum=TestMessage.Enum(int32_enum=1),
                              params=TestMessage.Params(int32_param=2),
                              mapping={'key': 'value'},
                              string_repeated=['hello', 'bye'])

        serialize(stream, message)

        stream.seek(0)
        contents = stream.read(-1)
        self.assertEqual(
            b'\n\x02\x10\x01\x12\x02\x10\x02'
            b'\x1a\x0c\n\x03key\x12\x05value"\x05hello"\x03b'
            b'ye', contents)

    def test_deserialize_fail_exceeds_max_size(self):
        contents = io.BytesIO(b'\n\x02\x10\x01\x12\x02\x10\x02'
                              b'\x1a\x0c\n\x03key\x12\x05value"\x05hello"\x03b'
                              b'ye')

        with self.assertRaises(BufferError):
            deserialize(contents, TestMessage, max_size=16)

    def test_deserialize_ok(self):
        contents = io.BytesIO(b'\n\x02\x10\x01\x12\x02\x10\x02'
                              b'\x1a\x0c\n\x03key\x12\x05value"\x05hello"\x03b'
                              b'ye')
        deserialized = deserialize(contents, TestMessage)

        self.assertEqual(
            TestMessage(enum=TestMessage.Enum(int32_enum=1),
                        params=TestMessage.Params(int32_param=2),
                        mapping={'key': 'value'},
                        string_repeated=['hello', 'bye']), deserialized)


if __name__ == '__main__':
    unittest.main()
