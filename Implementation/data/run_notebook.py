import time
import nbformat
from datetime import datetime
from nbconvert.preprocessors import ExecutePreprocessor
import shutil
import os

notebook_path = "./main.ipynb"              # Path to your notebook
log_path = "./log_execution.txt"            # Log file
csv_file = "merged_data.csv"                # Main output file
backup_dir = "./backup"                     # Folder to store backups
execution_interval = 1                      # Run every second
backup_interval = 600                        # Backup every 60 loops

loop_counter = 0                            # Track loop iterations

# Ensure backup folder exists
os.makedirs(backup_dir, exist_ok=True)

while True:
    print("🔄 Running main.ipynb...")

    try:
        # Load and execute the notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        ep.preprocess(notebook)

        # Log success
        with open(log_path, "a") as log:
            log.write(f"{datetime.now()}: ✅ Notebook executed successfully\n")

        # 🔒 Create a backup of the CSV every N iterations
        if os.path.exists(csv_file) and loop_counter % backup_interval == 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.csv")
            shutil.copy(csv_file, backup_file)
            with open(log_path, "a") as log:
                log.write(f"{datetime.now()}: 🔒 Backup created: {backup_file}\n")

    except Exception as e:
        error_message = f"{datetime.now()}: ❌ Error running notebook: {e}"
        print(error_message)
        with open(log_path, "a") as log:
            log.write(error_message + "\n")
        time.sleep(5)  # prevent tight loop on failure

    # Wait before next execution
    time.sleep(execution_interval)
    loop_counter += 1
