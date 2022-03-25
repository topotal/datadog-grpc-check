FROM alphine as download-grpc-health-probe
ENV GRPC_HEALTH_PROBE_VERSION 0.4.8
ENV GRPC_HEALTH_PROBE_OS_ARCH linux-amd64
RUN wget -O /bin/grpc-health-probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-${GRPC_HEALTH_PROBE_OS_ARCH}

FROM gcr.io/datadoghq/agent:7

COPY --from=download-grpc-health-probe /bin/grpc-health-probe /bin/grpc-health-probe
RUN chmod +x /bin/grpc_health_probe

COPY checks.d/grpc_check.py /checks.d/grpc_check.py
