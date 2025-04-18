FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

ENV PROMETHEUS_VERSION=2.55.0

RUN apt-get update && \
    apt-get install -y wget python3 python3-pip && \
    wget -q https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.linux-$(dpkg --print-architecture).tar.gz && \
    tar xvfz prometheus-$PROMETHEUS_VERSION.linux-$(dpkg --print-architecture).tar.gz

CMD ["/bin/bash", "-c", "/mnt/metrics/metrics_init.sh"]

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.