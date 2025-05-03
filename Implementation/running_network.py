"""
Module for orchestrating UC simulations and logging their execution.
Compatible with macOS, Linux and Windows.
"""

import subprocess
import random
import time
from datetime import datetime
import os
import sys

# The list of user cases to run
UC_SCRIPTS = ["uc1.py", "uc2.py", "uc3.py", "uc4.py", "uc5.py", "uc6.py"]
LOG_DIR = os.path.join(".", "log")
LOG_FILE = os.path.join(LOG_DIR, "log_execution.log")


def init_log():
    """
    Initializes the log file and directory if needed.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} Starting new run...\n")


def run_simulation(script_name: str):
    """
    Runs the selected UC simulation and logs its outcome.

    Args:
        script_name (str): Name of the UC script to run.
    """
    start_time = datetime.now().isoformat()
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        end_time = datetime.now().isoformat()
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{end_time} — Finished {script_name}\n")
    except subprocess.CalledProcessError as e:
        end_time = datetime.now().isoformat()
        print(f"❌ Error while running {script_name}: {e}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{end_time} — Error while running {script_name}: {e}\n")


if __name__ == "__main__":
    init_log()

    while True:
        selected_uc = random.choice(UC_SCRIPTS)
        run_simulation(selected_uc)
        print(f"✅ Finished running {selected_uc}")
        time.sleep(random.randint(60, 120))
