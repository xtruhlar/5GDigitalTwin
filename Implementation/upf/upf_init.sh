#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)
export IF_NAME=$(ip r | awk '/default/ { print $5 }')

# Remove ogstun and ogstun2 if they exist
ip link delete ogstun
ip link delete ogstun2

python3 /mnt/upf/tun_if.py --tun_ifname ogstun --ipv4_range $UE_IPV4_INTERNET --ipv6_range 2001:230:cafe::/48
python3 /mnt/upf/tun_if.py --tun_ifname ogstun2 --ipv4_range $UE_IPV4_IMS --ipv6_range 2001:230:babe::/48 --nat_rule 'no'

UE_IPV4_INTERNET_TUN_IP=$(python3 /mnt/upf/ip_utils.py --ip_range $UE_IPV4_INTERNET)
UE_IPV4_IMS_TUN_IP=$(python3 /mnt/upf/ip_utils.py --ip_range $UE_IPV4_IMS)

cp /mnt/upf/upf.yaml install/etc/open5gs
sed -i 's|UPF_IP|'$UPF_IP'|g' install/etc/open5gs/upf.yaml
sed -i 's|SMF_IP|'$SMF_IP'|g' install/etc/open5gs/upf.yaml
sed -i 's|UE_IPV4_INTERNET_TUN_IP|'$UE_IPV4_INTERNET_TUN_IP'|g' install/etc/open5gs/upf.yaml
sed -i 's|UE_IPV4_INTERNET_SUBNET|'$UE_IPV4_INTERNET'|g' install/etc/open5gs/upf.yaml
sed -i 's|UE_IPV4_IMS_TUN_IP|'$UE_IPV4_IMS_TUN_IP'|g' install/etc/open5gs/upf.yaml
sed -i 's|UE_IPV4_IMS_SUBNET|'$UE_IPV4_IMS'|g' install/etc/open5gs/upf.yaml
sed -i 's|UPF_ADVERTISE_IP|'$UPF_ADVERTISE_IP'|g' install/etc/open5gs/upf.yaml
sed -i 's|MAX_NUM_UE|'$MAX_NUM_UE'|g' install/etc/open5gs/upf.yaml

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.