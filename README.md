# datadog-grpc-check

Agent check for Datadog that checks endpoint implemented [gRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md).

## Prerequirements

datadog-grpc-check uses [grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe) internal.

## Metrics

| Metrics                            | Description |
| ---------------------------------- | ----------- |
| network.grpc.response_time (gauge) | The response time (second) of an gRPC request to given target. |
| network.grpc.can_connect (guage)   | 1 if checks can connect and status success, 0 otherwise. |
