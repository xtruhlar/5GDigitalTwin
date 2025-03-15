#!/bin/bash

# Function to stop gNB
stop_gnb() {
    echo "Stopping gNB..."
    docker compose -f srsgnb_zmq.yaml down
}

# Function to stop Open5GS and other components
stop_open5gs() {
    echo "Stopping Open5GS and other components..."
    docker compose -f deploy-all.yaml down
}

# Stop gNB first
stop_gnb

# Stop Open5GS and other components
stop_open5gs

echo "All components have been stopped."