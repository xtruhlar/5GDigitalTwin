#!/bin/bash

export DB_URI="mongodb://${MONGO_IP}/open5gs"

cp /mnt/bsf/bsf.yaml install/etc/open5gs
sed -i 's|BSF_IP|'$BSF_IP'|g' install/etc/open5gs/bsf.yaml
sed -i 's|SCP_IP|'$SCP_IP'|g' install/etc/open5gs/bsf.yaml
sed -i 's|NRF_IP|'$NRF_IP'|g' install/etc/open5gs/bsf.yaml
sed -i 's|MONGO_IP|'$MONGO_IP'|g' install/etc/open5gs/bsf.yaml
sed -i 's|MAX_NUM_UE|'$MAX_NUM_UE'|g' install/etc/open5gs/bsf.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.