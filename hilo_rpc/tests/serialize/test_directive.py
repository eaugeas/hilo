import unittest

import os

from hilo_rpc.serialize.directive import EnvironDirective


class DirectiveTest(unittest.TestCase):
    def test_environ_directive_ok_use_passed_env(self):
        directive = EnvironDirective('env', *['$PROPERTY'], **{
            'env': {'PROPERTY': 'VALUE'}
        })
        value = directive.execute()
        self.assertEqual(value, 'VALUE')

    def test_environ_directive_ok_use_os_environ(self):
        os.environ['PROPERTY'] = 'VALUE'
        directive = EnvironDirective('env', *['$PROPERTY'], **{
            'use_os_environ': True
        })
        value = directive.execute()
        self.assertEqual(value, 'VALUE')

    def test_environ_directive_fail_no_env_variable(self):
        directive = EnvironDirective('env', *['$PROPERTY'], **{
            'env': {}
        })
        with self.assertRaises(KeyError):
            directive.execute()


if __name__ == '__main__':
    unittest.main()
