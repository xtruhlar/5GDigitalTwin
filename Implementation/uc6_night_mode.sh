#!/bin/bash

# Worst-case scenario: 1 UE, sleep for 5 minutes
# bash uc6_night_mode.sh 0.08s user 0.05s system 0% cpu 5:05.44 total

echo "🌙 Night quiet mode — only one UE connects"
docker compose -f nr-UEs/nr-ue1.yaml -p night up --build -d
sleep 5
echo "✅ Single UE connected"

echo "🕒 Simulating quiet activity for 5 minutes..."
sleep 300

echo "🛑 Ending quiet mode"
docker compose -p night down