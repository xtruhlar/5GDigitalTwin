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
docker compose -f nr-gnb.yaml up -d && docker container attach nr_gnb

# UERANSIM NR-UE (RF simulated)
docker compose -f nr-UEs/nr-ue1.yaml -p ues up --build -d

# UC 1 - 6
```


```

