#!/bin/bash

# === Default values ===
UE_COUNT=1
TRAFFIC_UE_COUNT=1
DOWNLOADS=1

# === Parse CLI args ===
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --ues) UE_COUNT="$2"; shift ;;
    --traffic-ues) TRAFFIC_UE_COUNT="$2"; shift ;;
    --downloads) DOWNLOADS="$2"; shift ;;
    *) echo "❌ Unknown parameter: $1"; exit 1 ;;
  esac
  shift
done

echo "🚀 UC4 Traffic Simulation: Launching $UE_COUNT UEs"
echo "🌐 Simulating traffic in $TRAFFIC_UE_COUNT UEs with $DOWNLOADS downloads each"
echo "------------------------------------------------------------"

# === Start UEs ===
for ((i=1; i<=UE_COUNT; i++)); do
  echo "🔹 Starting nr-ue$i..."
  docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation up --build -d
done

echo "✅ All $UE_COUNT UEs launched!"
echo "⏳ Waiting 5 seconds before traffic begins..."
sleep 5

# === Simulate traffic ===
for ((i=1; i<=TRAFFIC_UE_COUNT; i++)); do
  CONTAINER="nr_ue${i}"
  echo "📡 Simulating traffic in $CONTAINER..."

docker exec "$CONTAINER" bash -c \
  "for i in \$(seq 1 $DOWNLOADS); do echo \"Downloading #\$i...\"; curl -4 -s -o /dev/null http://speedtest.tele2.net/1MB.zip; echo \"✅ Done #\$i\"; done" &
done

wait
echo "✅ Traffic simulation complete for selected UEs."
