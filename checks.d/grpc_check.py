import time

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.utils.subprocess_output import get_subprocess_output


class GrpcCheck(AgentCheck):

    METRICS_CAN_CONNECT = 'network.grpc.can_connect'
    METRICS_RESPONSE_TIME = 'network.grpc.response_time'

    def __init__(self, name, init_config, instances):
        super(GrpcCheck, self).__init__(name, init_config, instances)

        instance = instances[0]
        self.server = instance.get('server')
        self.port = instance.get('port')
        self.service = instance.get('service')
        self.connect_timeout = instance.get('connent_timeout', 10)
        self.rpc_timeout = instance.get('rpc_timeout', 10)

        if not self.server:
            raise ConfigurationError("'server' must be specified")
        if not self.port:
            raise ConfigurationError("'port' must be specified")

    def check(self, instance):
        command = self._build_command()

        start = time.time()
        output, err, retcode = get_subprocess_output(command, self.log, raise_on_empty_output=False)
        elapsed = time.time() - start

        tags = self._get_tags()

        # Handle exit codes.
        # see https://github.com/grpc-ecosystem/grpc-health-probe#exit-codes
        if retcode == 0:
            self.gauge(self.METRICS_CAN_CONNECT, 1, tags=tags)
            # Only report response_time metrics if can connect gRPC endpoint
            self.gauge(self.METRICS_RESPONSE_TIME, elapsed, tags=tags)
        elif retcode == 1:
            raise CheckException(err)
        else:
            self.gauge(self.METRICS_CAN_CONNECT, 0, tags=tags)

    def _build_command(self):
        addr = "{}:{}".format(self.server, self.port)
        command = ['grpc_health_probe', '-addr', addr]

        if self.service:
            command = command + ['-service', self.service]
        if self.connect_timeout:
            command = command + ['-connect-timeout', '{}s'.format(self.connect_timeout)]
        if self.rpc_timeout:
            command = command + ['-rpc-timeout', '{}s'.format(self.rpc_timeout)]
        return command

    def _get_tags():
        return ['service:{}'.format(self.service)] if self.service else None
