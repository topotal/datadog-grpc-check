import os
import sys
import unittest

sys.path.append('{}/../checks.d/'.format(os.path.dirname(__file__)))
import grpc_check

class TestGrpcCheck(unittest.TestCase):

    def test_build_command(self):
        instance = {
            'server': '192.0.2.10',
            'port': 50051,
            'service': 'helloworld.Greeter'
        }
        check = grpc_check.GrpcCheck('grpc_check', {}, [instance])

        actual = check._build_command()
        expected = 'grpc_health_probe -addr 192.0.2.10:50051 -service helloworld.Greeter -connect-timeout 10s -rpc-timeout 10s'.split(' ')
        self.assertEqual(actual, expected)
