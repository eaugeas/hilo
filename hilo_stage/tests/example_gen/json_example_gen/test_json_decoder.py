import unittest

import json

from hilo_stage.components.example_gen.json_example_gen.json_decoder import (
    ParseJsonLine)


class ParseJsonLineTest(unittest.TestCase):
    def test_process_ok_simple(self):
        parser = ParseJsonLine()
        parsed = next(parser.process('{"int": 1, "str": "s"}'))
        self.assertEqual(parsed, ['["int", 1]', '["str", "s"]'])

    def test_process_ok_sub_record(self):
        parser = ParseJsonLine()
        parsed = next(parser.process('{"object": {"int": 1, "str": "s"}}'))
        self.assertEqual(parsed, ['["object.int", 1]', '["object.str", "s"]'])

    def test_process_ok_sub_list(self):
        parser = ParseJsonLine()
        parsed = next(parser.process('{"list": ["1", "2", "3"]}'))
        self.assertEqual(parsed, ['["list", \"[\\"1\\", \\"2\\", \\"3\\"]\"]'])

    def test_process_fail_no_json(self):
        parser = ParseJsonLine()
        with self.assertRaises(json.decoder.JSONDecodeError):
            next(parser.process('{int: 1, str: s}'))


if __name__ == '__main__':
    unittest.main()
