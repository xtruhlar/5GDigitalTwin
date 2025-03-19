#!/bin/bash
# Check if Docker is logged in
if ! docker info > /dev/null 2>&1; then
    echo "You are not logged in to Docker. Please log in using 'docker login' and try again."
    exit 1
fi

# Start Open5GS and other components
docker compose -f deploy-all.yaml up --build -d
if [ $? -ne 0 ]; then
    echo "Failed to start Open5GS and other components. Please check the Docker Compose file and try again."
    exit 1
fi
echo "Open5GS and other components are starting..."

# Second flag is the number of UEs to connect
num_ues=3

# Time to load all components of Open5GS
sleep 10

if [[ "$1" == "-u" ]]; then
    # connect_ues.sh script
    ./connect_ues.sh $num_ues
fi