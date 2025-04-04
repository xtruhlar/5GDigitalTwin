#!/bin/bash

echo "🛑 Stopping UEs in parallel..."

# Default number of UEs
num_ues=100

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --ues) num_ues="$2"; shift ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

# Function to stop a single UE
stop_ue() {
  local ue_id=$1
  echo "🔻 Stopping nr-ue${ue_id}..."
  docker compose -f nr-UEs/nr-ue${ue_id}.yaml -p implementation down
  echo "✅ nr-ue${ue_id} stopped!"
}

# Loop to start threads for each UE
for ((i=1; i<=num_ues; i++)); do
  stop_ue "$i" &
  sleep 0.75
done

# Wait for all threads to complete
wait

echo "✅ All UEs stopped in parallel!"