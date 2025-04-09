import time
import subprocess

UC5_UE_COUNT = 8
UC5_DURATION = 300  # 5 minút

print(f"🚨 Starting UC5: Load Registration Anomaly with {UC5_UE_COUNT} UEs")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

# Spustenie všetkých UE paralelne
processes = []
for i in range(1, UC5_UE_COUNT + 1):
    cmd = ["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc5", "up", "--build", "-d"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append(proc)

# Počkaj na dokončenie všetkých paralelných subprocessov
for proc in processes:
    proc.communicate()

print("✅ All UEs connected nearly simultaneously.")
print("🕒 Holding all connections for UC5 duration...")
time.sleep(UC5_DURATION)

print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
print("🛑 UC5 complete. Stopping all UEs...")
subprocess.run(["docker", "compose", "-p", "uc5", "down"])

