#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue4.yaml /UERANSIM/config/ueransim-ue4.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue4.yaml

sed -i 's|UE4_KI|'$UE4_KI'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|UE4_OP|'$UE4_OP'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|UE4_AMF|'$UE4_AMF'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|UE4_IMEISV|'$UE4_IMEISV'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|UE4_IMEI|'$UE4_IMEI'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|UE4_IMSI|'$UE4_IMSI'|g' /UERANSIM/config/ueransim-ue4.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue4.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
