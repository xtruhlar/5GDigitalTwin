#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue3.yaml /UERANSIM/config/ueransim-ue3.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue3.yaml

sed -i 's|UE3_KI|'$UE3_KI'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|UE3_OP|'$UE3_OP'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|UE3_AMF|'$UE3_AMF'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|UE3_IMEISV|'$UE3_IMEISV'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|UE3_IMEI|'$UE3_IMEI'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|UE3_IMSI|'$UE3_IMSI'|g' /UERANSIM/config/ueransim-ue3.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue3.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.