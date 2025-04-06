#!/bin/bash

# BSD 2-Clause License

# Copyright (c) 2020, Supreeth Herle
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue252.yaml /UERANSIM/config/ueransim-ue252.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue252.yaml

sed -i 's|UE252_KI|'$UE252_KI'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|UE252_OP|'$UE252_OP'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|UE252_AMF|'$UE252_AMF'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|UE252_IMEISV|'$UE252_IMEISV'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|UE252_IMEI|'$UE252_IMEI'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|UE252_IMSI|'$UE252_IMSI'|g' /UERANSIM/config/ueransim-ue252.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue252.yaml

# Sync docker time
#ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /mnt/ueransim/timezone
