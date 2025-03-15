#!/bin/bash

# Function to connect a UE
connect_ue() {
    local ue_number=$1
    echo "Connecting UE${ue_number}..."
    if [[ "$ue_number" == "1" ]]; then
        osascript -e 'tell application "Terminal" to do script "cd /Users/davidtruhlar/Documents/FIIT/BP/5GDigitalTwin/Implementation && docker compose -f nr-ue.yaml up -d && docker container attach nr_ue"'
    else
        osascript -e 'tell application "Terminal" to do script "cd /Users/davidtruhlar/Documents/FIIT/BP/5GDigitalTwin/Implementation && docker compose -f nr-ue'${ue_number}'.yaml up -d && docker container attach nr_ue'${ue_number}'"'
    fi
    sleep 5
}

# Check if the argument is a number between 1 and 3
if [[ "$1" =~ ^[1-3]$ ]]; then
    echo "Connecting $1 UEs..."
    num_ues=$1
else
    echo "Usage: $0 -[1-3]"
    exit 1
fi

# Start nr-gnb before connecting UEs
osascript -e 'tell application "Terminal" to do script "cd /Users/davidtruhlar/Documents/FIIT/BP/5GDigitalTwin/Implementation && docker compose -f nr-gnb.yaml up -d && docker container attach nr_gnb"'
sleep 10


# Connect the specified number of UEs
for ((i=1; i<=num_ues; i++)); do
    connect_ue $i
done

sleep 10

# Start disconnecting the UEs
docker compose -f nr-ue.yaml down
sleep 5
docker compose -f nr-ue2.yaml down
sleep 5
docker compose -f nr-ue3.yaml down
sleep 5

# Disconnect the gNB and attach the terminal
#docker compose -f nr-gnb.yaml down

echo "All specified UEs have been connected and disconnected."