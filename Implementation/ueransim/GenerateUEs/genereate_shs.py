import os

# Directory to save the generated scripts
output_dir = "./ueransim/init_scripts"
os.makedirs(output_dir, exist_ok=True)

# Template for the init script
template = """#!/bin/bash

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

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
"""

# Generate 20 init scripts
for i in range(1, 11):
    file_content = template.format(index=i)
    file_path = os.path.join(output_dir, f"ueransim-ue{i}_init.sh")
    with open(file_path, "w") as file:
        file.write(file_content)
    # Make the script executable
    os.chmod(file_path, 0o755)

print(f"Generated 20 init scripts in {output_dir}")