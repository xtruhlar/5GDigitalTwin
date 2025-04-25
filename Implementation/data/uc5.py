import time
import subprocess
import random

UC5_UE_COUNT = 4
# UC5_DURATION = random.randint(300, 600)  # 10 min
UC5_DURATION = random.randint(60, 120)

print(f"🚨 Starting UC5: Load Registration Anomaly with {UC5_UE_COUNT} UEs")

with open("data/current_uc.txt", "w") as f:
    f.write("uc5")

# 🏁 Spustenie všetkých UE paralelne
processes = []
for i in range(1, UC5_UE_COUNT + 1):
    cmd = ["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc5", "up", "--build", "-d"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append(proc)

# ⏳ Počkaj na dokončenie všetkých paralelných subprocessov
for proc in processes:
    proc.communicate()

print("✅ All UEs connected nearly simultaneously.")
print("🕒 Holding all connections for UC5 duration...")
time.sleep(UC5_DURATION)

print("🛑 UC5 complete. Stopping all UEs...")
subprocess.run(["docker", "compose", "-p", "uc5", "down"])


with open("data/current_uc.txt", "w") as f:
    f.write("uc1")