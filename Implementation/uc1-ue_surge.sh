#!/bin/bash

echo "🚀 Launching 10 UEs with Docker Compose..."

for i in {1..10}; do
  echo "🔹 Starting nr-ue$i..."
  docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation up --build -d
  sleep 0.5
done

echo "✅ All UEs launched!"
