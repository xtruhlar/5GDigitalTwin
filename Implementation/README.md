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
docker compose -f nr-UEs/nr-ue1.yaml -p implementation up --build -d
# UC 1 - 6
```
#UC1
./uc1-surge.sh --ues 10

#UC2
./uc2-rampup.sh --ues 10 --interval 10

#UC3
./uc3-handover.sh --rounds 2 --wait 5

#UC4
./uc4-traffic.sh --ues 5 --traffic-ues 2 --downloads 10

#UC5
./uc5-idle.sh --time 300

#UC6
./uc6-reset.sh --ues 5 wait 5
```