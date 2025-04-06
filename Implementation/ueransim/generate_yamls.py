import os

# Directory to save the generated YAML files
output_dir = "./ueransim/yaml_configs"
os.makedirs(output_dir, exist_ok=True)

# Template for the YAML file
template = """# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 or 16 digits)
supi: 'imsi-UE{index}_IMSI'
# Mobile Country Code value of HPLMN
mcc: 'MCC'
# Mobile Network Code value of HPLMN (2 or 3 digits)
mnc: 'MNC'

# Permanent subscription key
key: 'UE{index}_KI'
# Operator code (OP or OPC) of the UE
op: 'UE{index}_OP'
# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OP'
# Authentication Management Field (AMF) value
amf: 'UE{index}_AMF'
# IMEI number of the device. It is used if no SUPI is provided
imei: 'UE{index}_IMEI'
# IMEISV number of the device. It is used if no SUPI and IMEI is provided
imeiSv: 'UE{index}_IMEISV'

# List of gNB IP addresses for Radio Link Simulation
gnbSearchList:
  - NR_GNB_IP

# UAC Access Identities Configuration
uacAic:
  mps: false
  mcs: false

# UAC Access Control Class
uacAcc:
  normalClass: 0
  class11: false
  class12: false
  class13: false
  class14: false
  class15: false

# Initial PDU sessions to be established
sessions:
  - type: 'IPv4'
    apn: 'internet'
    slice:
      sst: 1

# Configured NSSAI for this UE by HPLMN
configured-nssai:
  - sst: 1

# Default Configured NSSAI for this UE
default-nssai:
  - sst: 1

# Supported encryption algorithms by this UE
integrity:
  IA1: true
  IA2: true
  IA3: true

# Supported integrity algorithms by this UE
ciphering:
  EA1: true
  EA2: true
  EA3: true

# Integrity protection maximum data rate for user plane
integrityMaxRate:
  uplink: 'full'
  downlink: 'full'
"""

# Generate 20 YAML files
for i in range(1, 257):
    file_content = template.format(index=i)
    file_path = os.path.join(output_dir, f"ueransim-ue{i}.yaml")
    with open(file_path, "w") as file:
        file.write(file_content)

print(f"Generated 20 YAML files in {output_dir}")