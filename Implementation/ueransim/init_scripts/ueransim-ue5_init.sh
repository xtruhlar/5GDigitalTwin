#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue5.yaml /UERANSIM/config/ueransim-ue5.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue5.yaml

sed -i 's|UE5_KI|'$UE5_KI'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|UE5_OP|'$UE5_OP'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|UE5_AMF|'$UE5_AMF'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|UE5_IMEISV|'$UE5_IMEISV'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|UE5_IMEI|'$UE5_IMEI'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|UE5_IMSI|'$UE5_IMSI'|g' /UERANSIM/config/ueransim-ue5.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue5.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
