#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue100.yaml /UERANSIM/config/ueransim-ue100.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue100.yaml

sed -i 's|UE100_KI|'$UE100_KI'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|UE100_OP|'$UE100_OP'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|UE100_AMF|'$UE100_AMF'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|UE100_IMEISV|'$UE100_IMEISV'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|UE100_IMEI|'$UE100_IMEI'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|UE100_IMSI|'$UE100_IMSI'|g' /UERANSIM/config/ueransim-ue100.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue100.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
