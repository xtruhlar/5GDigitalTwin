#!/bin/bash

# Function to run a specific UE
run_ue() {
    local ue_number=$1
    echo "Starting UE${ue_number}..."
    docker compose -f nr-UEs/nr-ue${ue_number}.yaml -p implementation up --build -d
}

# Run the selected UEs
run_ue 1
run_ue 10
run_ue 100
run_ue 500

echo "Started UE1, UE10, UE100, and UE500."./uc