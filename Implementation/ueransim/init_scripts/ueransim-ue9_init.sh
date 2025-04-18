#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue9.yaml /UERANSIM/config/ueransim-ue9.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue9.yaml

sed -i 's|UE9_KI|'$UE9_KI'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|UE9_OP|'$UE9_OP'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|UE9_AMF|'$UE9_AMF'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|UE9_IMEISV|'$UE9_IMEISV'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|UE9_IMEI|'$UE9_IMEI'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|UE9_IMSI|'$UE9_IMSI'|g' /UERANSIM/config/ueransim-ue9.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue9.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
