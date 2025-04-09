import subprocess
import time
import random

UE_COUNT = 5
SESSION_DURATION = 600  # 10 minút worst case
STREAM_MB_PER_SESSION = (100, 200)

print(f"📺 Starting Video Streaming (UC2) with {UE_COUNT} UEs")

# Spustenie všetkých UEs
for i in range(1, UE_COUNT + 1):
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc2", "up", "--build", "-d"])
    print(f"✅ UE{i} started")

# Paralelné streamovanie
for i in range(1, UE_COUNT + 1):
    data_mb = random.randint(*STREAM_MB_PER_SESSION)
    ue_name = f"nr_ue{i}"
    print(f"🎬 UE{i} streaming {data_mb}MB")
    subprocess.run(["docker", "exec", "-d", ue_name, "bash", "-c", f"dd if=/dev/urandom bs=1M count={data_mb} of=/dev/null"])

print(f"🕒 Letting streams run for {SESSION_DURATION} seconds...")
time.sleep(SESSION_DURATION)

print("🛑 UC2 complete. Stopping all UEs...")
subprocess.run(["docker", "compose", "-p", "uc2", "down"])