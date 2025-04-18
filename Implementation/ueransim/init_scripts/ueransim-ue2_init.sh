#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue2.yaml /UERANSIM/config/ueransim-ue2.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue2.yaml

sed -i 's|UE2_KI|'$UE2_KI'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|UE2_OP|'$UE2_OP'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|UE2_AMF|'$UE2_AMF'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|UE2_IMEISV|'$UE2_IMEISV'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|UE2_IMEI|'$UE2_IMEI'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|UE2_IMSI|'$UE2_IMSI'|g' /UERANSIM/config/ueransim-ue2.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue2.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.