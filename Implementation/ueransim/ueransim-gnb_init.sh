#!/bin/bash

export IP_ADDR=$(awk 'END{print $1}' /etc/hosts)

cp /mnt/ueransim/${COMPONENT_NAME}.yaml /UERANSIM/config/${COMPONENT_NAME}.yaml
cp /mnt/ueransim/deregister.sh /UERANSIM/deregister.sh
chmod +x /UERANSIM/deregister.sh  # Make the script executable

sed -i 's|MNC|'$MNC'|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|MCC|'$MCC'|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|NR_GNB_IP|'$NR_GNB_IP'|g' /UERANSIM/config/${COMPONENT_NAME}.yaml
sed -i 's|AMF_IP|'$AMF_IP'|g' /UERANSIM/config/${COMPONENT_NAME}.yaml

echo "🚀 Starting gNB process..."
# Run gNB as background process
./nr-gnb -c ../config/${COMPONENT_NAME}.yaml > /mnt/ueransim/gnb.log 2>&1 &

# Wait until NG Setup is successful
until grep -q "NG Setup procedure is successful" /mnt/ueransim/gnb.log; do
    echo "⏳ Waiting for NG Setup success in gnb.log..."
    sleep 1
done

echo "✅ gNB connected to AMF"

# Start the exporter (background)
echo "📊 Launching ues.py Prometheus exporter..."
python3 /mnt/ueransim/ues.py &

# ✅ Now instead of bash, use wait on the gNB
wait %1  # Keeps container running tied to nr-gnb process
