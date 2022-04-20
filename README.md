# datadog-grpc-check

Agent check for Datadog that checks endpoint implemented [gRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md).

## Prerequirements

datadog-grpc-check uses [grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe) internal.

## Configuration

- [Configuration sample](conf.d/grpc_check.yaml.example)

| Setting                          | Description |
| -------------------------------- | ----------- |
| server (Required)                | Hostname or IP address of gRPC endpoint to check. |
| port (Required)                  | Port to check. |
| connect_timeout                  | Value of `--connect-timeout` option of grpc-health-probe (second). see [grpc-ecosystem/grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe#other-available-flags) |
| rpc_timeout                      | Value of `--rpc-timeout` option of grpc-health-probe (second). see [grpc-ecosystem/grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe#other-available-flags) |
| collect_grpc_health_probe_status | Enable collect status of grpc_heath_probe. |
| tags                             | List of tags. |

## Metrics

| Metrics                                          | Description |
| ------------------------------------------------ | ----------- |
| network.grpc.response_time (gauge)               | The response time (second) of a gRPC request to given target. |
| network.grpc.can_connect (gauge)                 | 1 if checks can connect and status success, 0 otherwise. |
| network.grpc.grpc_health_probe_status.0 (gauge)  | grpc_health_probe status 0. |
| network.grpc.grpc_health_probe_status.1 (gauge)  | grpc_health_probe status 1. |
| network.grpc.grpc_health_probe_status.2 (gauge)  | grpc_health_probe status 2. |
| network.grpc.grpc_health_probe_status.3 (gauge)  | grpc_health_probe status 3. |
| network.grpc.grpc_health_probe_status.4 (gauge)  | grpc_health_probe status 4. |
| network.grpc.grpc_health_probe_status.20 (gauge) | grpc_health_probe status 20. |
