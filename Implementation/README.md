### Build Docker images from source
```
cd /base
docker build --no-cache --force-rm -t docker_open5gs .

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
# UERANSIM gNB (RF simulated)
docker compose -f nr-gnb.yaml -p gnodeb up -d && docker container attach nr_gnb

# UERANSIM NR-UE (RF simulated)
docker compose -f nr-UEs/nr-ue1.yaml -p ues up --build -d

# UC 1 - 6

# Obnova databázy
```
docker cp ./mongodb_backup/open5gs mongo:/data/backup/open5gs
docker exec -it mongo mongorestore --uri="mongodb://localhost:27017" /data/backup/open5gs
```