import subprocess
import time
import random

# Constants
UE_COUNT = 4
SESSION_DURATION = random.randint(300, 600)

def run_uc2():

    """
    Run UC2: Video Streaming scenario.

    Simulates a typical video streaming session where all UEs continuously receive data.
    This scenario helps to evaluate throughput and session stability under constant load.

    Scenario Summary
        - Starts 4 UEs using Docker Compose.
        - Each UE downloads 2MB of random data every second.
        - Streaming duration is randomized between 300 and 600 seconds.
        - The UC label is logged into 'data/current_uc.txt'.

    Args
        None

    Returns
        None
    """

    print(f"📺 Starting Video Streaming (UC2) with {UE_COUNT} UEs")

    with open("data/current_uc.txt", "w") as f:
        f.write("uc2")

    # First, run all UEs
    for i in range(1, UE_COUNT + 1):
        subprocess.run(["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc2", "up", "--build", "-d"])
        print(f"✅ UE{i} started")

    # Then, simulate network activity
    print(f"🕒 Letting streams run for {SESSION_DURATION} seconds...")
    start_time = time.time()
    while time.time() - start_time < SESSION_DURATION:
        for i in range(1, UE_COUNT + 1):
            ue_name = f"nr_ue{i}"
            print(f"🎬 UE{i} downloading 2MB")
            subprocess.run(["docker", "exec", "-d", ue_name, "bash", "-c", "dd if=/dev/urandom bs=1M count=2 of=/dev/null"])
        time.sleep(1)  # Simulate some delay between downloads

    print("🛑 UC2 complete. Stopping all UEs...")
    subprocess.run(["docker", "compose", "-p", "uc2", "down"])

    with open("data/current_uc.txt", "w") as f:
        f.write("uc1")


if __name__ == "__main__":
    run_uc2()