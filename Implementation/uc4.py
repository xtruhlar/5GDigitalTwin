"""
UC4 - Short Burst Sessions
This script simulates short burst sessions for a specified number of UEs (User Equipment).
"""

import subprocess
import time
import random

# Constants
BURST_UE_COUNT = 4
BURST_DURATION = random.randint(300, 600)


def run_uc4():

    """Run the UC4 scenario with short burst sessions."""

    print(f"⚡ Starting UC4: Short Burst Sessions with {BURST_UE_COUNT} UEs")

    with open("data/current_uc.txt", "w") as f:
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

    with open("data/current_uc.txt", "w") as f:
        f.write("uc1")


if __name__ == "__main__":
    run_uc4()