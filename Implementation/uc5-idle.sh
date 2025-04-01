#!/bin/bash

# === UC5: Network Idle State ===
# Description: No UEs connected for a specific duration

# Default wait time (in seconds)
DURATION=300

# Parse CLI arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -t|--time)
      DURATION="$2"
      shift 2
      ;;
    *)
      echo "Unknown parameter passed: $1"
      echo "Usage: ./uc5_idle.sh [-t|--time <seconds>]"
      exit 1
      ;;
  esac
done

echo "🛑 Ensuring no UE containers are running..."
for i in {1..10}; do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation down
done

echo "🌙 Network is now idle. Countdown:"

# Countdown loop
for ((i=DURATION; i>0; i--)); do
  printf "\r⏳ Remaining idle time: %4d seconds" "$i"
  sleep 1
done

echo -e "\n✅ UC5 completed: Idle period finished."
