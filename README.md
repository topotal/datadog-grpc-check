# datadog-grpc-check

Agent check for Datadog that checks endpoint implemented [gRPC Health Checking Protocol](https://github.com/grpc/grpc/blob/master/doc/health-checking.md).

## Prerequirements

datadog-grpc-check uses [grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe) internal.

## Configuration

- [Configuration sample](conf.d/grpc_check.yaml.example)

| Setting           | Description |
| ------------------| ----------- |
| server (Required)                 | Hostname or IP address of gRPC endpoint to check. |
| port (Required)                   | Port to check. |
| connect_timeout                   | Value of `--connect-timeout` option of grpc-health-probe (second). see [grpc-ecosystem/grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe#other-available-flags) |
| rpc_timeout                       | Value of `--rpc-timeout` option of grpc-health-probe (second). see [grpc-ecosystem/grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe#other-available-flags) |
| probe_extra_args                  | Array of other arguments to send to grpc-health-probe. see [grpc-ecosystem/grpc-health-probe](https://github.com/grpc-ecosystem/grpc-health-probe#other-available-flags) |
| tags                              | List of tags. |
| collect_grpc_health_probe_status  | Collect grpc-health-probe CLI exit code and errors count metrics. Default: False |

## Metrics

| Metrics                                   | Description |
| ----------------------------------        | ----------- |
| network.grpc.response_time (gauge)        | The response time (second) of a gRPC request to given target. |
| network.grpc.can_connect (gauge)          | 1 if checks can connect and status success, 0 otherwise. |
| network.grpc.health.exit_code (gauge)     | grpc-health-probe CLI exit code|
| network.grpc.health.errors (count)        | Number of non-zero exit codes returned|


