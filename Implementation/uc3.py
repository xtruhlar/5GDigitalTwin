import subprocess
import time
import random

# Constants
UE_COUNT = 4
SESSION_DURATION = random.randint(300, 600)
PING_INTERVAL_MIN = 30
PING_INTERVAL_MAX = 35
TARGET_URL = "https://phet-dev.colorado.edu/html/build-an-atom/0.0.0-3/simple-text-only-test-page.html"

def run_uc3():

    """
    Run UC3: Periodic Keep-Alive scenario.

    Simulates multiple UEs that periodically send HTTP requests (keep-alive pings) to a remote server.
    This pattern reflects real-world background traffic in mobile applications (e.g. chat apps, weather updates).

    Scenario Summary
        - Starts 4 UEs as containers using Docker Compose.
        - Each UE sends periodic HTTP GET requests (via `curl`) to a predefined URL.
        - The interval between pings is randomized between 30–35 seconds.
        - Simulation duration is randomly set between 300–600 seconds.
        - Scenario type is logged into 'data/current_uc.txt'.

    Args
        None
        
    Returns
        None
    """
    
    print(f"📡 Starting Periodic Keep-Alive (UC3) with {UE_COUNT} UEs")

    with open("data/current_uc.txt", "w") as f:
        f.write("uc3")


    # Start UEs
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
    subprocess.run(["docker", "compose", "-p", "uc3", "down"])


    with open("data/current_uc.txt", "w") as f:
        f.write("uc1")


if __name__ == "__main__":
    run_uc3()