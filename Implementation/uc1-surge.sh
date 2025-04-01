#!/bin/bash

# === DEFAULTS ===
UE_COUNT=10

# === PARSE FLAGS ===
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --ues)
      UE_COUNT="$2"
      shift 2
      ;;
    *)
      echo "❌ Unknown argument: $1"
      echo "Usage: $0 [--ues N]"
      exit 1
      ;;
  esac
done

echo "🚀 Launching $UE_COUNT UEs with Docker Compose..."

for ((i=1; i<=UE_COUNT; i++)); do
  echo "🔹 Starting nr-ue$i..."
  docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation up --build -d
  sleep 0.5
done

echo "✅ $UE_COUNT UEs launched!"
