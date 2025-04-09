# UC1 - Normálne surfovanie
#!/bin/bash

UE_COUNT=25
SESSION_DURATION=960  # 16 minút worst case
DOWNLOAD_INTERVAL_MIN=60
DOWNLOAD_INTERVAL_MAX=120

echo "🌐 Starting Normal Surfing (UC1) with $UE_COUNT UEs"

# Na začiatku pripojme polovicu UE
for ((i=1; i<=UE_COUNT/2; i++)); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p uc1 up --build -d
  echo "✅ UE$i started"
done

START_TIME=$(date +%s)
while true; do
  NOW=$(date +%s)
  ELAPSED=$((NOW - START_TIME))
  if [ "$ELAPSED" -ge "$SESSION_DURATION" ]; then
    break
  fi

  for ((i=1; i<=UE_COUNT; i++)); do
    # Ak kontajner beží, náhodne stiahni dáta
    docker ps --format '{{.Names}}' | grep -q "nr_ue${i}"
    if [ $? -eq 0 ]; then
      if (( RANDOM % 10 < 3 )); then
        DATA_MB=$((RANDOM % 45 + 5))
        echo "📥 UE$i downloading ${DATA_MB}MB"
        docker exec -d nr_ue${i} bash -c "dd if=/dev/urandom bs=1M count=$DATA_MB of=/dev/null"
      fi

      # Občasné odpojenie
      if (( RANDOM % 100 < 2 )); then
        echo "❌ UE$i disconnecting..."
        docker compose -f nr-UEs/nr-ue${i}.yaml -p uc1 down
      fi
    else
      # Občasné pripojenie odpojených UE
      if (( RANDOM % 100 < 2 )); then
        echo "🔌 UE$i connecting..."
        docker compose -f nr-UEs/nr-ue${i}.yaml -p uc1 up --build -d
      fi
    fi
  done

  SLEEP_TIME=$((RANDOM % (DOWNLOAD_INTERVAL_MAX - DOWNLOAD_INTERVAL_MIN + 1) + DOWNLOAD_INTERVAL_MIN))
  sleep "$SLEEP_TIME"
done

echo "🛑 UC1 complete. Stopping all UEs..."
docker compose -p uc1 down