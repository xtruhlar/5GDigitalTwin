#!/bin/bash

# === DEFAULT CONFIG ===
NUM_UES=2
WAIT_SECONDS=5

# === CLI PARSING ===
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -n|--ues) NUM_UES="$2"; shift ;;
        -w|--wait) WAIT_SECONDS="$2"; shift ;;
        *) echo "❌ Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "🧾 Config: NUM_UES=$NUM_UES | WAIT=$WAIT_SECONDS seconds"

# === UC6 LOGIC ===

echo "❌ Stopping all UE containers..."
./stop_all_ues.sh
sleep 1

echo "❌ Stopping gNB..."
docker compose -f nr-gnb.yaml down 
sleep 1

echo "🔁 Restarting AMF, SMF, UPF..."
docker compose -f deploy-all.yaml restart amf 
docker compose -f deploy-all.yaml restart smf 
docker compose -f deploy-all.yaml restart upf 
sleep 2

echo "🕒 Simulating network outage. Waiting $WAIT_SECONDS seconds..."
for ((i=WAIT_SECONDS; i>0; i--)); do
  echo -ne "⏳ $i seconds remaining...\r"
  sleep 1
done

echo -e "\n📡 Starting gNB..."
docker compose -f nr-gnb.yaml up -d
sleep 5  # Wait for NG setup

echo "🚀 Starting UE containers..."
for i in $(seq 1 $NUM_UES); do
  docker compose -f nr-UEs/nr-ue${i}.yaml -p implementation up -d
  sleep 0.5
done

echo "✅ UC6: Network recovery simulation complete."
