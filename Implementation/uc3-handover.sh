#!/bin/bash

# === DEFAULTS ===
WAIT=5
ROUNDS=3

GROUP_A=(1 2 3)
GROUP_B=(4 5 6)
GROUP_C=(7 8 9 10)

# === PARSE FLAGS ===
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --wait)
      WAIT="$2"
      shift 2
      ;;
    --rounds)
      ROUNDS="$2"
      shift 2
      ;;
    *)
      echo "❌ Unknown argument: $1"
      echo "Usage: $0 [--wait N] [--rounds N]"
      exit 1
      ;;
  esac
done

echo "🚦 Simulating UE Handover (Wait: $WAIT s, Rounds: $ROUNDS)..."

run_group() {
  local group_name=$1[@]
  local group=("${!group_name}")

  echo "🔌 Disconnecting all UEs..."
  for i in {1..10}; do
    docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation down
  done

  echo "⏳ Waiting before new group starts..."
  sleep "$WAIT"

  echo "🚀 Starting UE group: ${group[*]}"
  for i in "${group[@]}"; do
    docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation up -d
  done
}

# === Emulate Handover ===
for ((round = 1; round <= ROUNDS; round++)); do
  echo "🔁 Round $round - Activating GROUP A..."
  run_group GROUP_A
  sleep "$WAIT"

  echo "🔁 Round $round - Activating GROUP B..."
  run_group GROUP_B
  sleep "$WAIT"

  echo "🔁 Round $round - Activating GROUP C..."
  run_group GROUP_C
  sleep "$WAIT"
done

echo "✅ UC3 simulation complete."
