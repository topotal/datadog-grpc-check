import time

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.utils.subprocess_output import get_subprocess_output


__version__ = '0.0.1'

METRICS_CAN_CONNECT = 'network.grpc.can_connect'
METRICS_RESPONSE_TIME = 'network.grpc.response_time'


def build_command(server, port, service, connect_timeout, rpc_timeout):
    addr = "{}:{}".format(server, port)
    command = ['grpc_health_probe', '-addr', addr]

    if service:
        command = command + ['-service', service]
    if connect_timeout:
        command = command + ['-connect-timeout', '{}s'.format(connect_timeout)]
    if rpc_timeout:
        command = command + ['-rpc-timeout', '{}s'.format(rpc_timeout)]
    return command


class GrpcCheck(AgentCheck):

    def check(self, instance):
        server = instance.get('server')
        port = instance.get('port')
        service = instance.get('service')
        connect_timeout = instance.get('connent_timeout', 10)
        rpc_timeout = instance.get('rpc_timeout', 10)

        if not server:
            raise ConfigurationError("'server' must be specified")
        if not port:
            raise ConfigurationError("'port' must be specified")

        command = build_command(server, port, service, connect_timeout, rpc_timeout)

        start = time.time()
        output, err, retcode = get_subprocess_output(command, self.log, raise_on_empty_output=False)
        elapsed = time.time() - start

        tags = ['service:{}'.format(service)] if service else None

        # Handle exit codes.
        # see https://github.com/grpc-ecosystem/grpc-health-probe#exit-codes
        if retcode == 0:
            self.gauge(METRICS_CAN_CONNECT, 1, tags=tags)
            # Only report response_time metrics if can connect gRPC endpoint
            self.gauge(METRICS_RESPONSE_TIME, elapsed, tags=tags)
        elif retcode == 1:
            raise CheckException(err)
        else:
            self.gauge(METRICS_CAN_CONNECT, 0, tags=tags)
