# `Research in the field of Digital Twin technology`
Bachelor's thesis, Faculty of informatics and information technologies

## Author: David Truhlar, Supervisor: Ing. Matej Petrik

### Digital Twin (Core + UERANSIM + Grafana, Loki and custom  metrics + LSTM real-time classification with online fine-tunning)

#### Platform compatibility
This project was tested on:
- macOS Sequoya Version 15.4 (24E248)
- Ubuntu 22.04.3 LTS (Jammy Jellyfish)
- Windows is not supported (EOF is not compatible with Windows)

#### Prerequisites
- git (version 2.39.5)
- docker (version 28.0.1)

#### Step 1: Clone repository
```bash
git clone https://github.com/xtruhlar/5GDigitalTwin.git
cd 5GDigitalTwin/Implementation 
```

#### Step 2: Build Docker images
```bash
cd ./base
docker build -t docker_open5gs .

cd ../ueransim
docker build -t docker_ueransim .

cd ..
```

#### Step 3: Set `.env` variables
```bash
set -a
source .env
set +a
```

#### Step 4: Docker compose
```bash
docker compose -f deploy-all.yaml up --build -d
```

#### Step 5: Add subscribers to MongoDB
```bash
docker exec -it mongo mkdir -p /data/backup
docker cp ./mongodb_backup/open5gs mongo:/data/backup/open5gs
docker exec -it mongo mongorestore --uri="mongodb://localhost:27017" --db open5gs /data/backup/open5gs
```

To ensure everything work properly open http://localhost:9999/ in your browser and login using credentials:
	
Login: `admin`
Password: `1423`

#### Step 6: Connect UERANSIM gNB to Open5GS Core
```bash
docker compose -f nr-gnb.yaml -p gnodeb up -d && docker container attach nr_gnb
```

#### Step 7: Connect with registered UERANSIM UE 
```bash
docker compose -f nr-UEs/nr-ue1.yaml -p ues up --build -d
```

Then go to Grafana, open http://localhost:3000/ in your browser and login using credentials:
	
Login: `open5gs`
Password: `open5gs`

Open menu on the left, click on `Dashboards`. Select `Current state Dash` and you can see the current state of your 5G network.

### Repository structure
<pre>
.
├── Analytical part
│   ├── Overleaf components
│   └── FIIT_BP_DT5G.pdf # Bachelor's thesis pdf document
│           ├── 🔴 Technical Abstract
│           ├── 🔴 Lay Summary
│           ├── 🟢 Introduction
│           ├── 🟢 Problem statement
│           ├── 🟢 Technical literature review
│           ├── 🟢 Solution overview - high level
│           ├── 🟢 Risk assessment
│           ├── 🟢 Experimental reproducibility and integration
│           ├── 🟢 Sustainability and environmental impact
│           ├── 🟢 Employability
│           ├── 🟢 Teamwork, diversity and inclusion
│           └── 🟢 Conclusion
</pre>