#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue6.yaml /UERANSIM/config/ueransim-ue6.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue6.yaml

sed -i 's|UE6_KI|'$UE6_KI'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|UE6_OP|'$UE6_OP'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|UE6_AMF|'$UE6_AMF'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|UE6_IMEISV|'$UE6_IMEISV'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|UE6_IMEI|'$UE6_IMEI'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|UE6_IMSI|'$UE6_IMSI'|g' /UERANSIM/config/ueransim-ue6.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue6.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
