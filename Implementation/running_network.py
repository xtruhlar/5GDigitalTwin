import subprocess
import random
import time
from datetime import datetime

# The list of user cases to run
uc_scripts = ["uc1.py", "uc2.py", "uc3.py", "uc4.py", "uc5.py", "uc6.py"]
log_file = "./log/log_execution.log"

while True:
    selected_uc = random.choice(uc_scripts)
    start_time = datetime.now().isoformat()

    with open(log_file, "a") as log:
        log.write(f"{start_time} — Started {selected_uc}\n")

    try:
        result = subprocess.run(["python", selected_uc], check=True)
        end_time = datetime.now().isoformat()
        with open(log_file, "a") as log:
            log.write(f"{end_time} — Finished {selected_uc}\n")
    except subprocess.CalledProcessError as e:
        end_time = datetime.now().isoformat()
        print(f"❌ Error while running {selected_uc}: {e}")
        with open(log_file, "a") as log:
            log.write(f"{end_time} — Error while running {selected_uc}: {e}\n")
    time.sleep(random.randint(60, 600))

