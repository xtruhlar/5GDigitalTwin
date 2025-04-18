import os

# Output file for the generated variables
output_file = "./generated_ues.env"

# Base values
base_ip = [172, 22, 0, 43]  # Starting IP address as a list of octets
base_imsi = "001011234567"
base_ki = "8baf473f2f8fd09487cccbd7097c6"
base_op = "11111111111111111111111111111"
base_amf = "8000"
base_imei = "356938035643803"
base_imeisv = "4370816125816151"

# Function to increment the IP address
def increment_ip(ip):
    ip[3] += 1
    if ip[3] > 255:  # If the last octet exceeds 255, reset it and increment the next octet
        ip[3] = 0
        ip[2] += 1
    return ip

# Generate 10 UEs
with open(output_file, "w") as file:
    for i in range(1, 10):
        # Generate IP address
        ip = ".".join(map(str, base_ip))
        base_ip = increment_ip(base_ip)

        # Generate IMSI
        imsi = f"{base_imsi}{i:03d}"  # Pad with leading zeros to maintain length

        # Generate KI
        ki = f"{base_ki}{i:03d}"  # Pad with leading zeros to maintain length

        # Generate OP
        op = f"{base_op}{i:03d}"  # Pad with leading zeros to maintain length

        # AMF remains constant
        amf = base_amf

        # IMEI remains constant
        imei = base_imei

        # IMEISV remains constant
        imeisv = base_imeisv

        # Write to file
        file.write(f"NR_UE{i}_IP={ip}\n")
        file.write(f"UE{i}_IMSI={imsi}\n")
        file.write(f"UE{i}_KI={ki}\n")
        file.write(f"UE{i}_OP={op}\n")
        file.write(f"UE{i}_AMF={amf}\n")
        file.write(f"UE{i}_IMEI={imei}\n")
        file.write(f"UE{i}_IMEISV={imeisv}\n\n")

print(f"Generated 10 UEs in {output_file}")