#!/bin/bash

cp /mnt/udm/udm.yaml install/etc/open5gs
sed -i 's|UDM_IP|'$UDM_IP'|g' install/etc/open5gs/udm.yaml
sed -i 's|SCP_IP|'$SCP_IP'|g' install/etc/open5gs/udm.yaml
sed -i 's|NRF_IP|'$NRF_IP'|g' install/etc/open5gs/udm.yaml
sed -i 's|MAX_NUM_UE|'$MAX_NUM_UE'|g' install/etc/open5gs/udm.yaml

cp /mnt/udm/curve25519-1.key install/etc/open5gs/hnet
cp /mnt/udm/secp256r1-2.key install/etc/open5gs/hnet

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.