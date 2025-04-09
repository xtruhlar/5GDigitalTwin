#!/bin/bash

# Worst-case scenario: 10 UEs, sleep for 1 second, then send 200 MB of data + 300 seconds
# bash uc5_bg_activity.sh  1.05s user 0.49s system 0% cpu 5:24.75 total

UE_COUNT=10
for ((i=1; i<=$UE_COUNT; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p background up --build -d
  echo "✅ UE$i started"
  sleep 1
  docker exec -d nr_ue${i} bash -c 'timeout 300 bash -c "while true; do echo \"🔁 Background ping from UE$i\"; sleep 60; done"'
done

echo "🕒 Letting background UEs run for 5 minutes..."
sleep 300

echo "🛑 Stopping background UEs..."
docker compose -p background down
