#!/bin/bash

# Worst-case scenario: (80 UEs, 3s sleep) + 30s for stability
# bash uc3_morning_rush.sh  6.55s user 2.57s system 2% cpu 5:18.67 total

echo "🌅 Morning Rush — simulating registrations 7:00–9:00"

for ((i=1; i<=80; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p rush up --build -d
  echo "✅ UE$i registered"
  sleep $((RANDOM % 3 + 1))
done

sleep 30

echo "🌐 All 80 UEs registered."