#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue10.yaml /UERANSIM/config/ueransim-ue10.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue10.yaml

sed -i 's|UE10_KI|'$UE10_KI'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|UE10_OP|'$UE10_OP'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|UE10_AMF|'$UE10_AMF'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|UE10_IMEISV|'$UE10_IMEISV'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|UE10_IMEI|'$UE10_IMEI'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|UE10_IMSI|'$UE10_IMSI'|g' /UERANSIM/config/ueransim-ue10.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue10.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.