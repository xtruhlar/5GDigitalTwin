#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue8.yaml /UERANSIM/config/ueransim-ue8.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue8.yaml

sed -i 's|UE8_KI|'$UE8_KI'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|UE8_OP|'$UE8_OP'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|UE8_AMF|'$UE8_AMF'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|UE8_IMEISV|'$UE8_IMEISV'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|UE8_IMEI|'$UE8_IMEI'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|UE8_IMSI|'$UE8_IMSI'|g' /UERANSIM/config/ueransim-ue8.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue8.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.