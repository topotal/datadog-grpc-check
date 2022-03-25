from concurrent import futures
import os
import sys
import unittest
from unittest.mock import ANY, Mock, patch

import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

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
            'service': 'helloworld.GreeterHealthy'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        m_gauge.assert_any_call('network.grpc.can_connect', 1, tags=['addr:localhost:50051', 'service:helloworld.GreeterHealthy'])
        m_gauge.assert_any_call('network.grpc.response_time', ANY, tags=['addr:localhost:50051', 'service:helloworld.GreeterHealthy'])

    @patch('grpc_check.GrpcCheck._gauge')
    def test_grpc_health_probe_unhealty(self, m_gauge):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterUnhealthy'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])
        check.check(instance)

        m_gauge.assert_any_call('network.grpc.can_connect', 0, tags=['addr:localhost:50051', 'service:helloworld.GreeterUnhealthy'])

    def test_grpc_health_probe_invalid_option(self):
        instance = {
            'server': 'localhost',
            'port': 50051,
            'service': 'helloworld.GreeterHealthy',
            'connect_timeout': 'invalid_option'

        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        with self.assertRaises(CheckException) as e:
            check.check(instance)
