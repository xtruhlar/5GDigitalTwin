#!/bin/bash

# # Worst-case scenario: (10 UEs, 5 minutes each with 60s sleep)
# bash uc2_keep_alive.sh  0.89s user 0.41s system 0% cpu 5:34.76 total

UE_COUNT=10
for ((i=1; i<=$UE_COUNT; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p keepalive up --build -d
  echo "✅ UE${i} started with background traffic"
  sleep 2
  docker exec -d nr_ue${i} bash -c 'while true; do echo "📩 Keep-alive ping from UE$i"; sleep $((RANDOM % 60 + 60)); done'
done

echo "🕒 Letting UEs run for 5 minutes..."
sleep 300

echo "🛑 Stopping keep-alive UEs..."
docker compose -p keepalive down