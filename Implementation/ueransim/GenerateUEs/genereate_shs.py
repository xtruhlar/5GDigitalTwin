import os

# Directory to save the generated scripts
output_dir = "./ueransim/init_scripts"
os.makedirs(output_dir, exist_ok=True)

# Template for the init script
template = """#!/bin/bash

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

export IP_ADDR=$(awk 'END{{print $1}}' /etc/hosts)

cp /mnt/ueransim/yaml_configs/ueransim-ue{index}.yaml /UERANSIM/config/ueransim-ue{index}.yaml

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/ueransim-ue{index}.yaml

sed -i 's|UE{index}_KI|'$UE{index}_KI'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|UE{index}_OP|'$UE{index}_OP'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|UE{index}_AMF|'$UE{index}_AMF'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|UE{index}_IMEISV|'$UE{index}_IMEISV'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|UE{index}_IMEI|'$UE{index}_IMEI'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|UE{index}_IMSI|'$UE{index}_IMSI'|g' /UERANSIM/config/ueransim-ue{index}.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/ueransim-ue{index}.yaml

# Sync docker time
#ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /mnt/ueransim/timezone
"""

# Generate 20 init scripts
for i in range(1, 257):
    file_content = template.format(index=i)
    file_path = os.path.join(output_dir, f"ueransim-ue{i}_init.sh")
    with open(file_path, "w") as file:
        file.write(file_content)
    # Make the script executable
    os.chmod(file_path, 0o755)

print(f"Generated 20 init scripts in {output_dir}")