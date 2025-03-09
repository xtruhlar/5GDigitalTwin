#!/bin/bash

# Define the path to the netdata.conf file
NETDATA_CONF="/etc/netdata/netdata.conf"

# Update the netdata.conf file with the Prometheus IP
sed -i "s|http://<PROMETHEUS_IP>:9090/api/v1/write|http://${METRICS_IP}:9090/api/v1/write|g" $NETDATA_CONF

# Start NetData
/usr/sbin/netdata -D