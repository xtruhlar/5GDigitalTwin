"""
UC5 - Load Registration Anomaly
This script simulates a load registration anomaly by starting multiple UE instances
"""

import time
import subprocess
import random

# Constants
UC5_UE_COUNT = 4
UC5_DURATION = random.randint(300, 600)

def run_uc5():

    """Run the UC5 scenario with multiple UEs."""

    print(f"🚨 Starting UC5: Load Registration Anomaly with {UC5_UE_COUNT} UEs")

    with open("data/current_uc.txt", "w") as f:
        f.write("uc5")

    # Run all UEs in parallel
    processes = []
    for i in range(1, UC5_UE_COUNT + 1):
        cmd = ["docker", "compose", "-f", f"nr-UEs/nr-ue{i}.yaml", "-p", "uc5", "up", "--build", "-d"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(proc)

    # Wait for all UEs to finish starting
    for proc in processes:
        proc.communicate()

    print("✅ All UEs connected nearly simultaneously.")
    print("🕒 Holding all connections for UC5 duration...")
    time.sleep(5)

    print("🛑 UC5 complete. Stopping all UEs...")
    subprocess.run(["docker", "compose", "-p", "uc5", "down"])


    with open("data/current_uc.txt", "w") as f:
        f.write("uc1")


if __name__ == "__main__":
    run_uc5()