#!/bin/bash

export PROMETHEUS_WORK_DIR=prometheus-$PROMETHEUS_VERSION.linux-$(dpkg --print-architecture)
cd $PROMETHEUS_WORK_DIR

mkdir -p /config

cp /mnt/metrics/prometheus.yml /config/

sed -i 's|AMF_IP|'$AMF_IP'|g' /config/prometheus.yml
sed -i 's|SMF_IP|'$SMF_IP'|g' /config/prometheus.yml
sed -i 's|MME_IP|'$MME_IP'|g' /config/prometheus.yml
sed -i 's|PCF_IP|'$PCF_IP'|g' /config/prometheus.yml
sed -i 's|UPF_IP|'$UPF_IP'|g' /config/prometheus.yml
sed -i 's|NETWORK_WATCHER_IP|'$NETWORK_WATCHER_IP'|g' /config/prometheus.yml

./prometheus --config.file=/config/prometheus.yml --web.enable-remote-write-receiver --storage.tsdb.allow-overlapping-blocks

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.