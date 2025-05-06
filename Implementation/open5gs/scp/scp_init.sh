#!/bin/bash

cp /mnt/scp/scp.yaml install/etc/open5gs
sed -i 's|SCP_IP|'$SCP_IP'|g' install/etc/open5gs/scp.yaml
sed -i 's|NRF_IP|'$NRF_IP'|g' install/etc/open5gs/scp.yaml
sed -i 's|MAX_NUM_UE|'$MAX_NUM_UE'|g' install/etc/open5gs/scp.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.