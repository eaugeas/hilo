import unittest

import io

from hilo_rpc.proto.tests_pb2 import TestMessage
from hilo_rpc.serialize.text import deserialize, serialize


class TextTest(unittest.TestCase):
    def test_serialize_ok(self):
        stream = io.StringIO()
        message = TestMessage(
            enum=TestMessage.Enum(int32_enum=1),
            params=TestMessage.Params(int32_param=2),
            mapping={'key': 'value'},
            string_repeated=['hello', 'bye']
        )

        serialize(stream, message)

        stream.seek(0)
        contents = stream.read(-1)
        self.assertEqual("""enum {
  int32_enum: 1
}
params {
  int32_param: 2
}
mapping {
  key: \"key\"
  value: \"value\"
}
string_repeated: \"hello\"
string_repeated: \"bye\"
""", contents)

    def test_deserialize_fail_exceeds_max_size(self):
        contents = io.StringIO("""enum {
          int32_enum: 1
        }
        params {
          int32_param: 2
        }
        mapping {
          key: \"key\"
          value: \"value\"
        }
        string_repeated: \"hello\"
        string_repeated: \"bye\"
        """)

        with self.assertRaises(BufferError):
            deserialize(contents, TestMessage, max_size=16)

    def test_deserialize_ok(self):
        contents = io.StringIO("""enum {
  int32_enum: 1
}
params {
  int32_param: 2
}
mapping {
  key: \"key\"
  value: \"value\"
}
string_repeated: \"hello\"
string_repeated: \"bye\"
""")
        deserialized = deserialize(contents, TestMessage)

        self.assertEqual(TestMessage(
            enum=TestMessage.Enum(int32_enum=1),
            params=TestMessage.Params(int32_param=2),
            mapping={'key': 'value'},
            string_repeated=['hello', 'bye']
        ), deserialized)


if __name__ == '__main__':
    unittest.main()
