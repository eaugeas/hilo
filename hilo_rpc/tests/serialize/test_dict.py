import unittest

from hilo_rpc.proto.tests_pb2 import TestMessage
from hilo_rpc.serialize.dict import (flatten, unflatten, deserialize,
                                     serialize, typedef)


class DictTest(unittest.TestCase):
    def test_serialize_ok_message(self):
        message = TestMessage(enum=TestMessage.Enum(int32_enum=1),
                              params=TestMessage.Params(int32_param=2),
                              mapping={'key': 'value'},
                              string_repeated=['hello', 'bye'])
        d = serialize(message)
        self.assertEqual(
            {
                'enum': {
                    'int32_enum': 1
                },
                'params': {
                    'bool_param': False,
                    'int32_param': 2,
                    'string_param': ''
                },
                'mapping': {
                    'key': 'value'
                },
                'params_repeated': [],
                'params_map': {},
                'string_repeated': ['hello', 'bye'],
            }, d)

    def test_serialize_ok_message_type(self):
        d = serialize(TestMessage)
        self.assertEqual(
            {
                'enum': {
                    'bool_enum': False,
                    'int32_enum': 0,
                    'string_enum': ''
                },
                'params': {
                    'bool_param': False,
                    'int32_param': 0,
                    'string_param': ''
                },
                'mapping': {},
                'string_repeated': [],
                'params_repeated': [],
                'params_map': {}
            }, d)

    def test_serialize_ok_message_type_with_types(self):
        d = typedef(TestMessage)
        self.assertEqual(
            {
                'enum': {
                    'bool_enum': 'bool',
                    'int32_enum': 'int',
                    'string_enum': 'str'
                },
                'params': {
                    'bool_param': 'bool',
                    'int32_param': 'int',
                    'string_param': 'str'
                },
                'mapping': {
                    'str': 'str'
                },
                'params_map': {
                    'entry': {
                        'key': 'int',
                        'value': {
                            'bool_param': 'bool',
                            'int32_param': 'int',
                            'string_param': 'str'
                        }
                    }
                },
                'string_repeated': ['str'],
                'params_repeated': [{
                    'bool_param': 'bool',
                    'int32_param': 'int',
                    'string_param': 'str'
                }]
            }, d)

    def test_flatten_ok_without_namespace(self):
        d = {'empty': {'empty': False}, 'local_file': {'path': ''}}

        result = flatten(d)

        self.assertEqual({'empty.empty': False, 'local_file.path': ''}, result)

    def test_flatten_ok_with_namespace(self):
        d = {'empty': {'empty': False}, 'local_file': {'path': ''}}

        result = flatten(d, namespace='input_config')

        self.assertEqual(
            {
                'input_config.empty.empty': False,
                'input_config.local_file.path': ''
            }, result)

    def test_flatten_fail_with_class(self):
        d = {'key': TestMessage()}

        with self.assertRaises(ValueError):
            flatten(d)

    def test_unflatten_dict_ok_without_namespace(self):
        d = {'empty.empty': False, 'local_file.path': ''}

        result = unflatten(d)

        self.assertEqual(
            {
                'empty': {
                    'empty': False
                },
                'local_file': {
                    'path': ''
                }
            }, result)

    def test_unflatten_ok_with_namespace(self):
        d = {
            'input_config.empty.empty': False,
            'input_config.local_file.path': ''
        }

        result = unflatten(d, namespace='input_config')

        self.assertEqual(
            {
                'empty': {
                    'empty': False
                },
                'local_file': {
                    'path': ''
                }
            }, result)

    def test_unflatten_fail_with_multilevel_dict(self):
        d = {'empty': {'empty': False}, 'local_file': {'path': ''}}

        with self.assertRaises(ValueError):
            unflatten(d)

    def test_deserialize_ok(self):
        deserialized = deserialize(
            {
                'enum': {
                    'bool_enum': True
                },
                'params': {
                    'bool_param': True,
                    'int32_param': 1,
                    'string_param': 'hello'
                },
                'mapping': {
                    'key': 'value'
                },
                'string_repeated': ['hello', 'bye'],
                'params_map': {
                    1: {
                        'bool_param': True,
                        'int32_param': 1,
                        'string_param': 'hello'
                    }
                }
            }, TestMessage)

        self.assertEqual(
            TestMessage(enum=TestMessage.Enum(bool_enum=True),
                        params=TestMessage.Params(bool_param=True,
                                                  int32_param=1,
                                                  string_param='hello'),
                        mapping={'key': 'value'},
                        string_repeated=['hello', 'bye'],
                        params_map={
                            1:
                            TestMessage.Params(bool_param=True,
                                               int32_param=1,
                                               string_param='hello')
                        }), deserialized)


if __name__ == '__main__':
    unittest.main()
