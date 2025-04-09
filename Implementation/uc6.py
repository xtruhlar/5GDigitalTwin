import time
import subprocess

AUTH_FAIL_UE_ID = 100  # predpokladáme, že pre UC6 máš vytvorený samostatný súbor (napr. s nevalidným IMSI)
AUTH_FAIL_RETRIES = 3
AUTH_FAIL_INTERVAL = 30  # každých 30s nový pokus
AUTH_FAIL_DURATION = 240  # 4 minúty max

print(f"🔒 Starting UC6: Authentication Failure Alert (max {AUTH_FAIL_RETRIES} retries)")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

start_time = time.time()
retry = 0

while retry < AUTH_FAIL_RETRIES and time.time() - start_time < AUTH_FAIL_DURATION:
    print(f"🔁 Attempt {retry + 1} — Starting UE{AUTH_FAIL_UE_ID}")
    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{AUTH_FAIL_UE_ID}.yaml", "-p", "uc6", "up", "--build", "-d"])
    time.sleep(10)  # krátka doba na zlyhanie autentifikácie
    subprocess.run(["docker", "compose", "-p", "uc6", "down"])
    retry += 1
    time.sleep(AUTH_FAIL_INTERVAL)
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

print("🛑 UC6 complete.")
