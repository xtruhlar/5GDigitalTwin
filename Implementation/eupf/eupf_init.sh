#!/bin/bash

export PATH="/usr/local/go/bin:${PATH}"
export PATH=$(go env GOPATH)/bin:${PATH}
export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)
export IF_NAME=$(ip r | awk '/default/ { print $5 }')

exec ./bin/eupf \
    --iface $IF_NAME \
    --aaddr $UPF_IP:8181 \
    --paddr $UPF_IP:8805 \
    --maddr $UPF_IP:9091 \
    --nodeid $UPF_IP \
    --ueip false \
    --ftup false \
    --loglvl info \
    --n3addr $UPF_ADVERTISE_IP $@

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.