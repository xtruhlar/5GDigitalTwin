#!/bin/bash

for i in {1..10}; do
  CONTAINER="nr_ue${i}"
  echo "📡 Simulating traffic in $CONTAINER..."

  # Simulate traffic using curl
  docker exec "$CONTAINER" bash -c "for i in {1..5}; do curl -s -o /dev/null http://speedtest.tele2.net/10MB.zip; done" &
done

# Wait for all background processes to complete
wait
echo "✅ Traffic simulation complete for all UEs."