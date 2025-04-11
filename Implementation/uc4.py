import subprocess
import time
import random

BURST_UE_COUNT = 4
BURST_DURATION = 600  # 10 min

print(f"⚡ Starting UC4: Short Burst Sessions with {BURST_UE_COUNT} UEs")

with open("current_uc.txt", "w") as f:
    f.write("uc4")

start_time = time.time()
while time.time() - start_time < BURST_DURATION:
    selected_ue = random.randint(1, BURST_UE_COUNT)
    print(f"🔌 UE{selected_ue} starting short session...")
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{selected_ue}.yaml", "-p", "uc4", "up", "--build", "-d"])
    subprocess.run(["docker", "exec", "-d", f"nr_ue{selected_ue}", "bash", "-c", "dd if=/dev/urandom bs=1M count=2 of=/dev/null"])
    time.sleep(random.randint(2, 4))
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{selected_ue}.yaml", "-p", "uc4", "down"])
    print(f"❌ UE{selected_ue} session ended")
    time.sleep(random.randint(3, 6))

print("🛑 UC4 complete.")

with open("current_uc.txt", "w") as f:
    f.write("no_uc")