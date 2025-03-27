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

docker compose -f deploy-all.yaml up --build -d


###### 5G SA deployment

```
# srsRAN ZMQ gNB (RF simulated)
docker compose -f srsgnb_zmq.yaml up -d && docker container attach srsgnb_zmq
docker compose -f srsue_5g_zmq.yaml up -d && docker container attach srsue_5g_zmq



# UERANSIM gNB (RF simulated)
docker compose -f nr-gnb.yaml up -d && docker container attach nr_gnb

# UERANSIM NR-UE (RF simulated)
docker compose -f nr-ue.yaml up -d && docker container attach nr_ue
docker compose -f nr-ue2.yaml up -d && docker container attach nr_ue2
docker compose -f nr-ue3.yaml up -d && docker container attach nr_ue3
```