import unittest

from hilo_rpc.serialize.dict import (
    flatten,
    unflatten,
    deserialize,
    serialize)

from hilo_rpc.proto.storage_pb2 import (
    InputConfig, LocalFileConfig)
from hilo_rpc.proto.pipeline_pb2 import Pipeline, PipelineConfig
from hilo_rpc.proto.stage_pb2 import Stage


class SerializeTest(unittest.TestCase):
    def test_serialize_ok_message(self):
        message = InputConfig(local_file=LocalFileConfig(path='filepath'))
        d = serialize(message)
        self.assertEqual(d, {
            'empty': {'empty': False},
            'local_file': {'path': 'filepath'}
        })

    def test_serialize_ok_message_type(self):
        message_type = InputConfig
        d = serialize(message_type)
        self.assertEqual(d, {
            'empty': {'empty': False},
            'local_file': {'path': ''}
        })

    def test_flatten_ok_without_namespace(self):
        d = {
            'empty': {'empty': False},
            'local_file': {'path': ''}
        }

        result = flatten(d)

        self.assertEqual(result, {
            'empty.empty': False,
            'local_file.path': ''
        })

    def test_flatten_ok_with_namespace(self):
        d = {
            'empty': {'empty': False},
            'local_file': {'path': ''}
        }

        result = flatten(d, namespace='input_config')

        self.assertEqual(result, {
            'input_config.empty.empty': False,
            'input_config.local_file.path': ''
        })

    def test_flatten_fail_with_class(self):
        d = {'key': InputConfig()}

        with self.assertRaises(ValueError):
            flatten(d)

    def test_unflatten_dict_ok_without_namespace(self):
        d = {
            'empty.empty': False,
            'local_file.path': ''
        }

        result = unflatten(d)

        self.assertEqual(result, {
            'empty': {'empty': False},
            'local_file': {'path': ''}
        })

    def test_unflatten_ok_with_namespace(self):
        d = {
            'input_config.empty.empty': False,
            'input_config.local_file.path': ''
        }

        result = unflatten(d, namespace='input_config')

        self.assertEqual(result, {
            'empty': {'empty': False},
            'local_file': {'path': ''}
        })

    def test_unflatten_fail_with_multilevel_dict(self):
        d = {
            'empty': {'empty': False},
            'local_file': {'path': ''}
        }

        with self.assertRaises(ValueError):
            unflatten(d)

    def test_deserialize_ok(self):
        deserialized = deserialize({
            'name': 'pipeline',
            'config': {
                'params': {'enable_cache': True},
                'stages': [{'id': '0'}, {'id': '1'}, {'id': '2'}]
            }
        }, Pipeline)

        self.assertEqual(deserialized, Pipeline(
            name='pipeline',
            config=PipelineConfig(
                params={'enable_cache': True},
                stages=[Stage(id='0'), Stage(id='1'), Stage(id='2')])))


if __name__ == '__main__':
    unittest.main()
