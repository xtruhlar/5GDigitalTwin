#!/bin/bash

cp /mnt/ausf/ausf.yaml install/etc/open5gs
sed -i 's|AUSF_IP|'$AUSF_IP'|g' install/etc/open5gs/ausf.yaml
sed -i 's|SCP_IP|'$SCP_IP'|g' install/etc/open5gs/ausf.yaml
sed -i 's|NRF_IP|'$NRF_IP'|g' install/etc/open5gs/ausf.yaml
sed -i 's|MAX_NUM_UE|'$MAX_NUM_UE'|g' install/etc/open5gs/ausf.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.