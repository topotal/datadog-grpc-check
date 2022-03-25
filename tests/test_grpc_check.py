import os
import sys
import unittest

sys.path.append('{}/../checks.d/'.format(os.path.dirname(__file__)))
import grpc_check

class TestGrpcCheck(unittest.TestCase):

    def test_build_command(self):
        actual = grpc_check.build_command('192.0.2.10', '50051', 'helloworld.Greeter', '10', '10')
        expected = 'grpc_health_probe -addr 192.0.2.10:50051 -service helloworld.Greeter -connect-timeout 10s -rpc-timeout 10s'.split(' ')
        self.assertEqual(actual, expected)
