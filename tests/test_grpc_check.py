import os
import sys
import unittest
from unittest.mock import ANY, patch

sys.path.append('{}/../checks.d/'.format(os.path.dirname(__file__)))
import grpc_check

from datadog_checks.base import ConfigurationError
from datadog_checks.base.errors import CheckException


class TestGrpcCheck(unittest.TestCase):

    def test_constructor(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        self.assertEqual(check.server, '192.0.2.10')
        self.assertEqual(check.port, 50051)
        self.assertEqual(check.service, 'helloworld.Greeter')
        self.assertEqual(check.connect_timeout, 10)
        self.assertEqual(check.rpc_timeout, 10)
        self.assertEqual(check.collect_grpc_health_probe_status, False)
        self.assertEqual(check.tags, [])

    def test_constructor_param_timeout(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter',
            'connect_timeout': 100,
            'rpc_timeout': 200,
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        self.assertEqual(check.server, '192.0.2.10')
        self.assertEqual(check.port, 50051)
        self.assertEqual(check.service, 'helloworld.Greeter')
        self.assertEqual(check.connect_timeout, 100)
        self.assertEqual(check.rpc_timeout, 200)
        self.assertEqual(check.tags, [])

    def test_constructor_param_tags(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter',
            'tags': ['key1:val1', 'key2:val2'],
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        self.assertEqual(check.server, '192.0.2.10')
        self.assertEqual(check.port, 50051)
        self.assertEqual(check.service, 'helloworld.Greeter')
        self.assertEqual(check.tags, ['key1:val1', 'key2:val2'])

    def test_constructor_param_collect_grpc_health_probe_status(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter',
            'collect_grpc_health_probe_status': True,
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        self.assertEqual(check.collect_grpc_health_probe_status, True)

    def test_constructor_server_not_specified(self):
        instance = {
            'port': 50051,
        }

        with self.assertRaises(ConfigurationError) as e:
            grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = str(e.exception)
        expected = "'server' must be specified"
        self.assertEqual(actual, expected)

    def test_constructor_port_not_specified(self):
        instance = {
            'server': '192.0.2.10',
        }

        with self.assertRaises(ConfigurationError) as e:
            grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = str(e.exception)
        expected = "'port' must be specified"
        self.assertEqual(actual, expected)

    def test_build_command(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = check._build_command()
        expected = [
            'grpc-health-probe',
            '-addr',
            '192.0.2.10:50051',
            '-service',
            'helloworld.Greeter',
            '-connect-timeout',
            '10s',
            '-rpc-timeout',
            '10s',
        ]
        self.assertEqual(actual, expected)

    def test_get_tags(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = check._get_tags()
        expected = ['addr:192.0.2.10:50051', 'service:helloworld.Greeter']
        self.assertListEqual(actual, expected)

    def test_get_tags_tags_specified(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter',
            'tags': ['key1:val1', 'key2:val2'],
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = check._get_tags()
        expected = [
            'key1:val1', 'key2:val2', 'addr:192.0.2.10:50051',
            'service:helloworld.Greeter'
        ]
        self.assertListEqual(actual, expected)

    def test_get_tags_service_not_specified(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = check._get_tags()
        expected = ['addr:192.0.2.10:50051']
        self.assertListEqual(actual, expected)

    def test_constructor_param_probe_extra_args(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter',
            'connect_timeout': 100,
            'rpc_timeout': 200,
            'probe_extra_args': ['-tls', '-user-agent', 'custom-user-agent'],
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        self.assertEqual(check.server, '192.0.2.10')
        self.assertEqual(check.port, 50051)
        self.assertEqual(check.service, 'helloworld.Greeter')
        self.assertEqual(check.connect_timeout, 100)
        self.assertEqual(check.rpc_timeout, 200)
        self.assertEqual(check.probe_extra_args,
                         ['-tls', '-user-agent', 'custom-user-agent'])
        self.assertEqual(check.tags, [])

    @patch('grpc_check.GrpcCheck._gauge')
    @patch('grpc_check.get_subprocess_output')
    def test_check_can_connect(self, m_get_subprocess_output, m_gauge):
        m_get_subprocess_output.return_value = (None, None, 0)

        instance = {
            'server': '192.0.2.10',
            'port': 50051,
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        m_gauge.assert_any_call('network.grpc.can_connect',
                                1,
                                tags=['addr:192.0.2.10:50051'])
        m_gauge.assert_any_call('network.grpc.response_time',
                                ANY,
                                tags=['addr:192.0.2.10:50051'])

    @patch('grpc_check.GrpcCheck._gauge')
    @patch('grpc_check.get_subprocess_output')
    def test_check_cant_connect(self, m_get_subprocess_output, m_gauge):
        m_get_subprocess_output.return_value = (None, 'error', 2)

        instance = {
            'server': '192.0.2.10',
            'port': 50051,
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        m_gauge.assert_any_call('network.grpc.can_connect',
                                0,
                                tags=['addr:192.0.2.10:50051'])

    @patch('grpc_check.GrpcCheck._gauge')
    @patch('grpc_check.get_subprocess_output')
    def test_check_error(self, m_get_subprocess_output, m_gauge):
        m_get_subprocess_output.return_value = (None, 'error', 1)

        instance = {
            'server': '192.0.2.10',
            'port': 50051,
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        with self.assertRaises(CheckException):
            check.check(instance)
