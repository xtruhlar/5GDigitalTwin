import time
import random
import subprocess

# Constants
AUTH_FAIL_UE_ID = 100 # We "malformed" UE with ID 100
AUTH_FAIL_RETRIES = random.randint(3, 6)
AUTH_FAIL_INTERVAL = random.randint(5, 30)
AUTH_FAIL_DURATION = random.randint(120, 300)

def run_uc6():

    """
    Run UC6: Authentication Failure Alert scenario.

    Simulates an authentication failure event in a 5G network by repeatedly starting a misconfigured UE (User Equipment)
    that fails to register due to incorrect credentials or malformed configuration. This scenario is useful for testing 
    network response to repeated failed attempts and monitoring for anomaly detection mechanisms.

    Scenario Summary
        - Launches a specially prepared UE (ID=100) which is expected to fail authentication.
        - Repeats the process a random number of times (3 to 6 retries).
        - Between each attempt, the UE is stopped and a random interval (5–30 seconds) is observed.
        - Total scenario duration is also bounded by a global timeout (120–300 seconds).
        - All events are logged to the console and scenario type is saved to `data/current_uc.txt`.

    Args
        None

    Returns
        None
    """

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


if __name__ == "__main__":
    run_uc6()