#!/bin/bash

# Worst-case scenario: 200 UEs
# bash uc7_slow_ddos.sh  18.32s user 7.02s system 3% cpu 13:57.35 total

echo "🚨 Simulating Slow DDoS (200 UEs in 10 minutes)"

for ((i=1; i<=200; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p slowddos up --build -d
  echo "🚨 UE$i connected"
  sleep 3
  if (( i % 20 == 0 )); then
    echo "🔥 $i UEs already connected..."
  fi
done