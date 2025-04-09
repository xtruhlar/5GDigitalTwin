import os

# Directory to save the generated YAML files
output_dir = "./nr-UEs"
os.makedirs(output_dir, exist_ok=True)

# Template for the YAML file
template = """services:
  nr_ue{index}:
    image: docker_ueransim
    container_name: nr_ue{index}
    stdin_open: true
    tty: true
    volumes:
      - ../ueransim:/mnt/ueransim
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - ../.env
    environment:
      - COMPONENT_NAME=ueransim-ue{index}
    expose:
      - "4997/udp"
    cap_add:
      - NET_ADMIN
    privileged: true
    networks:
      default:
        ipv4_address: ${{NR_UE{index}_IP}}
networks:
  default:
      name: docker_open5gs_default 
      external: true
"""

# Generate 20 YAML files
for i in range(1, 257):
    file_content = template.format(index=i)
    file_path = os.path.join(output_dir, f"nr-ue{i}.yaml")
    with open(file_path, "w") as file:
        file.write(file_content)

print(f"Generated 20 YAML files in {output_dir}")