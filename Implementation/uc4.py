import subprocess
import time
import random

BURST_UE_COUNT = 8
BURST_DURATION = 600  # 10 min

print(f"⚡ Starting UC4: Short Burst Sessions with {BURST_UE_COUNT} UEs")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

start_time = time.time()
while time.time() - start_time < BURST_DURATION:
    selected_ue = random.randint(1, BURST_UE_COUNT)
    print(f"🔌 UE{selected_ue} starting short session...")
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{selected_ue}.yaml", "-p", "uc4", "up", "--build", "-d"])
    time.sleep(random.randint(2, 4))
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{selected_ue}.yaml", "-p", "uc4", "down"])
    print(f"❌ UE{selected_ue} session ended")
    time.sleep(random.randint(3, 6))

print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

print("🛑 UC4 complete.")
