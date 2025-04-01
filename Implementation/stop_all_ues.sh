#!/bin/bash

echo "🛑 Stopping 10 UEs in parallel..."

# Function to stop a single UE
stop_ue() {
  local ue_id=$1
  echo "🔻 Stopping nr-ue${ue_id}..."
  docker compose -f nr-UEs/nr-ue${ue_id}.yaml -p implementation down
  echo "✅ nr-ue${ue_id} stopped!"
}

# Loop to start threads for each UE
for i in {1..10}; do
  stop_ue "$i" &
done

# Wait for all threads to complete
wait

echo "✅ All UEs stopped in parallel!"