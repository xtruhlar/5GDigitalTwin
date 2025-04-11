import subprocess
import time
import random

UE_COUNT = 4
SESSION_DURATION = 600 
DOWNLOAD_INTERVAL_MIN = 10
DOWNLOAD_INTERVAL_MAX = 15

print(f"🌐 Starting Normal Surfing (UC1) with {UE_COUNT} UEs")

with open("current_uc.txt", "w") as f:
    f.write("uc1")

# Na začiatku pripojme polovicu UE
for i in range(1, UE_COUNT // 2 + 1):
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc1", "up", "--build", "-d"])
    print(f"✅ UE{i} started")

start_time = time.time()
while True:
    elapsed = time.time() - start_time
    if elapsed >= SESSION_DURATION:
        break

    print(f"⏳ UC1 running for {int(elapsed)} seconds...")

    for i in range(1, UE_COUNT + 1):        
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        running_containers = result.stdout.splitlines()
        ue_name = f"nr_ue{i}"

        if ue_name in running_containers:
            # Náhodné sťahovanie dát
            if random.randint(0, 9) < 3:
                data_mb = random.randint(5, 50)
                print(f"📥 UE{i} downloading {data_mb}MB")
                subprocess.run(["docker", "exec", "-d", ue_name, "bash", "-c", f"dd if=/dev/urandom bs=1M count={data_mb} of=/dev/null"])
                print(f"✅ UE{i} finished downloading {data_mb}MB")

            # Občasné odpojenie
            if random.randint(0, 99) < 4:
                print(f"❌ UE{i} disconnecting...")
                subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc1", "down"])
        else:
            # Občasné pripojenie
            if random.randint(0, 99) < 4:
                print(f"🔌 UE{i} connecting...")
                subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc1", "up", "--build", "-d"])

    sleep_time = random.randint(DOWNLOAD_INTERVAL_MIN, DOWNLOAD_INTERVAL_MAX)
    print(f"⏳ Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)

print("🛑 UC1 complete. Stopping all UEs...")
subprocess.run(["docker", "compose", "-p", "uc1", "down"])

with open("current_uc.txt", "w") as f:
    f.write("no_uc")