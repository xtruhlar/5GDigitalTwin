#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue7.yaml /UERANSIM/config/ueransim-ue7.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue7.yaml

sed -i 's|UE7_KI|'$UE7_KI'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|UE7_OP|'$UE7_OP'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|UE7_AMF|'$UE7_AMF'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|UE7_IMEISV|'$UE7_IMEISV'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|UE7_IMEI|'$UE7_IMEI'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|UE7_IMSI|'$UE7_IMSI'|g' /UERANSIM/config/ueransim-ue7.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue7.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.