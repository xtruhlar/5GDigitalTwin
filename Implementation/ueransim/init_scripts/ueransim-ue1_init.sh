#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue1.yaml /UERANSIM/config/ueransim-ue1.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue1.yaml

sed -i 's|UE1_KI|'$UE1_KI'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|UE1_OP|'$UE1_OP'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|UE1_AMF|'$UE1_AMF'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|UE1_IMEISV|'$UE1_IMEISV'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|UE1_IMEI|'$UE1_IMEI'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|UE1_IMSI|'$UE1_IMSI'|g' /UERANSIM/config/ueransim-ue1.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue1.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
