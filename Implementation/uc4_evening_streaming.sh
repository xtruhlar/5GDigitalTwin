#!/bin/bash

# Worst-case scenario: 20 UEs, sleep for 5 seconds, then send 200 MB of data + 120 seconds
# bash uc4_evening_streaming.sh  1.85s user 0.77s system 1% cpu 3:50.20 total

UE_COUNT=20
echo "🌆 Evening streaming — connecting $UE_COUNT UEs for long sessions"

for ((i=1; i<=$UE_COUNT; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p stream up --build -d
  echo "📺 UE$i started stream"
  sleep $((RANDOM % 5 + 1))
done

for ((i=1; i<=$UE_COUNT; i++)); do
  docker exec -d nr_ue${i} bash -c 'dd if=/dev/urandom bs=1M count=200 > /dev/null'
  echo "📤 UE$i streaming data"
done

sleep 120  # keep active for a while