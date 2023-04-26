# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2023-04

### Added
- Support grpc-health-probe CLI extra arguments
  - It's enabled by `probe_extra_args` option.

## [0.1.0] - 2022-09

### Added
- Support grpc-health-probe CLI exit code.
  - It's enabled by `collect_grpc_health_probe_status` option, append two metrics.
- New metrics
  - `network.grpc.health.errors(count)`: is incremented when grpc-health-probe CLI return non-zero exit codes.
  - `network.grpc.health.exit_code(gauge)`: grpc-health-probe CLI exit code

