#!/bin/bash

echo "🛑 Stopping UEs in parallel..."

# 💯 Prednastavený počet UE
num_ues=11

# 💬 Spracovanie argumentov príkazového riadku
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --ues) num_ues="$2"; shift ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

# 🛑 Funkcia na zastavenie UE
stop_ue() {
  local ue_id=$1
  echo "🔻 Stopping nr-ue${ue_id}..."
  docker compose -f nr-UEs/nr-ue${ue_id}.yaml -p slowddos down
  echo "✅ nr-ue${ue_id} stopped!"
}

# 🛑 Zastavenie všetkých UE v paralelných threadoch
for ((i=1; i<=num_ues; i++)); do
  stop_ue "$i" &
  sleep 0.75
done

# ⏳ Čakanie na dokončenie všetkých pozadí
wait

echo "✅ All UEs stopped in parallel!"