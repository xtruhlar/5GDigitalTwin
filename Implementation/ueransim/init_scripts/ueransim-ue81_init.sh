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

cp /mnt/ueransim/yaml_configs/${COMPONENT_NAME}.yaml /UERANSIM/config/${COMPONENT_NAME}.yaml

sed -i 's|MNC|01|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|MCC|001|g' /UERANSIM/config/${COMPONENT_NAME}.yaml

sed -i 's|UE81_KI|8baf473f2f8fd09487cccbd7097c6881|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|UE81_OP|11111111111111111111111111111181|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|UE81_AMF|8000|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|UE81_IMEISV|4370816125816151|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|UE81_IMEI|356938035643803|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|UE81_IMSI|001011234567881|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|NR_GNB_IP|172.22.0.23|g' /UERANSIM/config/${COMPONENT_NAME}.yaml

# Sync docker time
#ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /mnt/ueransim/timezone
