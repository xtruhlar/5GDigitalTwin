#!/bin/bash

# Worst case scenario: 30 UEs sending 200MB each
# bash uc8_traffic_burst.sh  2.60s user 1.21s system 3% cpu 1:36.77 total

echo "🚀 Traffic Burst with 30 UEs"
UE_COUNT=30

for ((i=1; i<=$UE_COUNT; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p burst up --build -d
  echo "📶 UE$i connected"
done

sleep 10

for ((i=1; i<=$UE_COUNT; i++)); do
  #docker exec -d nr_ue${i} bash -c 'dd if=/dev/urandom bs=1M count=$((RANDOM % 100 + 100)) > /dev/null'
  docker exec -d nr_ue${i} bash -c 'dd if=/dev/urandom bs=1M count=200 > /dev/null'
  echo "📤 UE$i burst sent"
done

sleep 60
docker compose -p burst down