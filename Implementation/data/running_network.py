import subprocess
import random
import time
from datetime import datetime

# Zoznam UC skriptov
uc_scripts = ["uc1.py", "uc2.py", "uc3.py", "uc4.py", "uc5.py", "uc6.py"]

log_file = "log/UC_execution.log"

print("🚀 Starting UC orchestrator... Press Ctrl+C to stop.")

while True:
    selected_uc = random.choice(uc_scripts)
    start_time = datetime.now().isoformat()
    print(f"\n▶️ {start_time} — Running {selected_uc}...")

    with open(log_file, "a") as log:
        log.write(f"{start_time} — Started {selected_uc}\n")

    try:
        result = subprocess.run(["python", selected_uc], check=True)
        end_time = datetime.now().isoformat()
        print(f"✅ {selected_uc} finished successfully.")
        with open(log_file, "a") as log:
            log.write(f"{end_time} — Finished {selected_uc}\n")
    except subprocess.CalledProcessError as e:
        end_time = datetime.now().isoformat()
        print(f"❌ Error while running {selected_uc}: {e}")
        with open(log_file, "a") as log:
            log.write(f"{end_time} — Error while running {selected_uc}: {e}\n")

    print("🕒 Sleeping for 30 seconds to allow network recovery...")
    time.sleep(30)
