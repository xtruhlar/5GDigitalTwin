#!/bin/bash

echo "🛑 Stopping 10 UEs..."

for i in {1..10}; do
  echo "🔻 Stopping nr-ue$i..."
  docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation down
done

echo "✅ All UEs stopped!"
