import time
import random
import subprocess

AUTH_FAIL_UE_ID = 100 # We "malformed" UE with ID 100
AUTH_FAIL_RETRIES = random.randint(3, 6)
AUTH_FAIL_INTERVAL = random.randint(5, 30)
AUTH_FAIL_DURATION = random.randint(120, 300)

print(f"🔒 Starting UC6: Authentication Failure Alert (max {AUTH_FAIL_RETRIES} retries)")

with open("data/current_uc.txt", "w") as f:
    f.write("uc6")
    
start_time = time.time()
retry = 0

while retry < AUTH_FAIL_RETRIES and time.time() - start_time < AUTH_FAIL_DURATION:
    print(f"🔁 Attempt {retry + 1} — Starting UE{AUTH_FAIL_UE_ID}")
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{AUTH_FAIL_UE_ID}.yaml", "-p", "uc6", "up", "--build", "-d"])
    time.sleep(10)  # Short delay to allow UE to start
    subprocess.run(["docker", "compose", "-p", "uc6", "down"])
    retry += 1
    time.sleep(AUTH_FAIL_INTERVAL)

print("🛑 UC6 complete.")

with open("data/current_uc.txt", "w") as f:
    f.write("uc1")