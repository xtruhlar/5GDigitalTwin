### Build Docker images from source
```
cd /base
docker build --no-cache --force-rm -t docker_open5gs .

cd ../ims_base
docker build --no-cache --force-rm -t docker_kamailio .

cd ../srslte
docker build --no-cache --force-rm -t docker_srslte .

cd ../srsran
docker build --no-cache --force-rm -t docker_srsran .

cd ../ueransim
docker build --no-cache --force-rm -t docker_ueransim .
```

#### Build docker images for additional components

```
cd ..
set -a
source .env
set +a
sudo sysctl -w net.inet.ip.forwarding=1

docker compose -f 4g-volte-deploy.yaml build
docker compose -f sa-deploy.yaml build
docker compose -f deploy-all.yaml build


docker compose -f deploy-all.yaml up --build -d

```

## Network Deployment

###### 4G deployment

```
# 4G Core Network + IMS + SMS over SGs (uses Kamailio IMS)
docker compose -f 4g-volte-deploy.yaml up

# 4G Core Network + IMS + SMS over SGs (uses openSIPS IMS)
docker compose -f 4g-volte-opensips-ims-deploy.yaml up

# srsRAN ZMQ eNB (RF simulated)
docker compose -f srsenb_zmq.yaml up -d && docker container attach srsenb_zmq

# srsRAN ZMQ 4G UE (RF simulated)
docker compose -f srsue_zmq.yaml up -d && docker container attach srsue_zmq
```

###### 5G SA deployment

```
# 5G Core Network
docker compose -f sa-deploy.yaml up

# srsRAN ZMQ gNB (RF simulated)
docker compose -f srsgnb_zmq.yaml up -d && docker container attach srsgnb_zmq

# srsRAN ZMQ 5G UE (RF simulated)
docker compose -f srsue_5g_zmq.yaml up -d && docker container attach srsue_5g_zmq

# UERANSIM gNB (RF simulated)
docker compose -f nr-gnb.yaml up -d && docker container attach nr_gnb

# UERANSIM NR-UE (RF simulated)
docker compose -f nr-ue.yaml up -d && docker container attach nr_ue
docker compose -f nr-ue2.yaml up -d && docker container attach nr_ue2
docker compose -f nr-ue3.yaml up -d && docker container attach nr_ue3
```