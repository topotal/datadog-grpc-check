from concurrent import futures
import os
import sys
import unittest
from unittest.mock import ANY, patch

import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from datadog_checks.base import AgentCheck
from datadog_checks.base.errors import CheckException

sys.path.append('{}/../checks.d/'.format(os.path.dirname(__file__)))
import grpc_check


class TestGrpcHealthProbe(unittest.TestCase):

    def setUp(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        server.add_insecure_port('localhost:50051')
        health_servicer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
        health_servicer.set('helloworld.GreeterHealthy', health_pb2.HealthCheckResponse.SERVING)
        health_servicer.set('helloworld.GreeterUnhealthy', health_pb2.HealthCheckResponse.NOT_SERVING)
        server.start()

    @patch('grpc_check.GrpcCheck._gauge')
    def test_grpc_health_probe_healty(self, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterHealthy',
            'collect_grpc_health_probe_status': False
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        expected_tags = ['addr:localhost:50051', 'service:helloworld.GreeterHealthy']
        m_gauge.assert_any_call('network.grpc.can_connect', 1, tags=expected_tags)
        m_gauge.assert_any_call('network.grpc.response_time', ANY, tags=expected_tags)

    @patch('grpc_check.GrpcCheck._gauge')
    def test_grpc_health_probe_healty_with_tags(self, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterHealthy',
            'tags': ['key1:val1', 'key2:val2'],
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        expected_tags = ['key1:val1', 'key2:val2', 'addr:localhost:50051', 'service:helloworld.GreeterHealthy']
        m_gauge.assert_any_call('network.grpc.can_connect', 1, tags=expected_tags)
        m_gauge.assert_any_call('network.grpc.response_time', ANY, tags=expected_tags)

    @patch('grpc_check.GrpcCheck._gauge')
    def test_grpc_health_probe_unhealty(self, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterUnhealthy'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        expected_tags = ['addr:localhost:50051', 'service:helloworld.GreeterUnhealthy']
        m_gauge.assert_any_call('network.grpc.can_connect', 0, tags=expected_tags)

    @patch('grpc_check.GrpcCheck._gauge')
    def test_grpc_health_probe_unhealty_with_tags(self, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterUnhealthy',
            'tags': ['key1:val1', 'key2:val2'],
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        expected_tags = ['key1:val1', 'key2:val2', 'addr:localhost:50051', 'service:helloworld.GreeterUnhealthy']
        m_gauge.assert_any_call('network.grpc.can_connect', 0, tags=expected_tags)

    @patch('grpc_check.GrpcCheck._gauge')
    @patch('datadog_checks.base.AgentCheck.count')
    def test_collect_health_probe_exit_code_metrics_when_collect_option_true(self, m_count, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterUnhealthy',
            'collect_grpc_health_probe_status': True
        }

        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        expected_tags = ['addr:localhost:50051', 'service:helloworld.GreeterUnhealthy']

        m_gauge.assert_any_call(grpc_check.GrpcCheck.METRICS_EXIT_CODE, 4, tags=expected_tags)
        m_count.assert_any_call(grpc_check.GrpcCheck.METRICS_ERRORS, 1, tags=expected_tags + ['grpc.health.exit_code:4'])

    @patch('grpc_check.GrpcCheck._gauge')
    @patch('datadog_checks.base.AgentCheck.count')
    def test_exit_code_tag_is_only_append_to_errors_metric(self, m_count, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterUnhealthy',
            'collect_grpc_health_probe_status': True
        }

        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        expected_tags = ['addr:localhost:50051', 'service:helloworld.GreeterUnhealthy']

        m_gauge.assert_any_call(grpc_check.GrpcCheck.METRICS_EXIT_CODE, 4, tags=expected_tags)
        m_count.assert_any_call(grpc_check.GrpcCheck.METRICS_ERRORS, 1, tags=expected_tags + ['grpc.health.exit_code:4'])


    @patch('datadog_checks.base.AgentCheck.count')
    @patch('grpc_check.GrpcCheck._gauge')
    def test_do_not_collect_when_option_false(self, m_gauge, m_count):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterUnhealthy',
            'collect_grpc_health_probe_status': False
        }

        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        m_count.assert_not_called()

    def test_grpc_health_probe_invalid_option(self):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterHealthy',
            'connect_timeout': 'invalid_option'

        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        with self.assertRaises(CheckException):
            check.check(instance)
