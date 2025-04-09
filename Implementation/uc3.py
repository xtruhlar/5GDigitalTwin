import subprocess
import time
import random

UE_COUNT = 8
SESSION_DURATION = 600  # 10 minút worst case
PING_INTERVAL_MIN = 30
PING_INTERVAL_MAX = 60
TARGET_URL = "https://phet-dev.colorado.edu/html/build-an-atom/0.0.0-3/simple-text-only-test-page.html"

print(f"📡 Starting Periodic Keep-Alive (UC3) with {UE_COUNT} UEs")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

# Spusti všetky UE
for i in range(1, UE_COUNT + 1):
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc3", "up", "--build", "-d"])
    print(f"✅ UE{i} started")

start_time = time.time()
while True:
    elapsed = time.time() - start_time
    if elapsed >= SESSION_DURATION:
        break

    for i in range(1, UE_COUNT + 1):
        ue_name = f"nr_ue{i}"
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        running_containers = result.stdout.splitlines()

        if ue_name in running_containers:
            print(f"📩 UE{i} sending keep-alive ping")
            subprocess.run(["docker", "exec", "-d", ue_name, "curl", "-s", TARGET_URL])

    sleep_time = random.randint(PING_INTERVAL_MIN, PING_INTERVAL_MAX)
    print(f"🕒 Sleeping for {sleep_time} seconds before next keep-alive round")
    time.sleep(sleep_time)

print("🛑 UC3 complete. Stopping all UEs...")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
subprocess.run(["docker", "compose", "-p", "uc3", "down"])

