import subprocess
import time
import random

# Constants
UE_COUNT = 4
SESSION_DURATION = random.randint(60, 600)
DOWNLOAD_INTERVAL_MIN = 5
DOWNLOAD_INTERVAL_MAX = 25

def run_uc1():

    """
    Run UC1: Normal Surfing scenario.

    Simulates user behavior with intermittent UE connectivity and randomized data downloads
    to mimic typical mobile web browsing patterns.

    Scenario Summary
        - Starts half of the UEs.
        - UEs may
            - download random chunks of data (5–50MB),
            - randomly disconnect or reconnect during the session.
        - The scenario runs for a randomized session duration (60–600 seconds).
        - Active UEs are defined in `nr-ue{i}.yaml` Docker Compose files.
        - Writes the current UC label to `data/current_uc.txt`.

    Args
        None

    Returns
        None
    """
    
    print(f"🌐 Starting Normal Surfing (UC1) with {UE_COUNT} UEs")
    with open("data/current_uc.txt", "w") as f:
        f.write("uc1")

    for i in range(1, UE_COUNT // 2 + 1):
        subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc1", "up", "--build", "-d"])
        print(f"✅ UE{i} started")

    start_time = time.time()
    while (time.time() - start_time) < SESSION_DURATION:
        for i in range(1, UE_COUNT + 1):
            ue_name = f"nr_ue{i}"
            containers = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True).stdout.splitlines()

            if ue_name in containers:
                if random.randint(0, 9) < 3:
                    data_mb = random.randint(5, 50)
                    subprocess.run(["docker", "exec", "-d", ue_name, "bash", "-c", f"dd if=/dev/urandom bs=1M count={data_mb} of=/dev/null"])
                if random.randint(0, 99) < 30:
                    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc1", "down"])
            else:
                if random.randint(0, 99) < 30:
                    subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc1", "up", "--build", "-d"])

        time.sleep(random.randint(DOWNLOAD_INTERVAL_MIN, DOWNLOAD_INTERVAL_MAX))

    subprocess.run(["docker", "compose", "-p", "uc1", "down"])
    with open("data/current_uc.txt", "w") as f:
        f.write("uc1")

if __name__ == "__main__":
    run_uc1()
