import time
import nbformat
from datetime import datetime
from nbconvert.preprocessors import ExecutePreprocessor
import shutil
import os

notebook_path = "./main.ipynb"              # Cesta k .ipynb
log_path = "./log_execution.log"            # Súbor pre logovanie
csv_file = "running_data.csv"               # Hlavný výstupný súbor
backup_dir = "./backup"                     # Priečinok na uloženie záloh
execution_interval = 1                      # Spustiť každú sekundu
backup_interval = 600                       # Zálohovať každých 600 sekúnd (10 minút)

loop_counter = 0                            # Počítadlo iterácií

# 📁 Zabezpečenie, že priečinok pre zálohy existuje
os.makedirs(backup_dir, exist_ok=True)

while True:
    print("🔄 Cyklus main.ipynb...")

    try:
        # 🔄 Načítanie a spustenie .ipynb
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        ep.preprocess(notebook)

        # 🪵 Zalogovať úspešné spustenie
        with open(log_path, "a") as log:
            log.write(f"{datetime.now()}: ✅ Notebook bol úspešne spustený\n")

        # 🔒 Vytvoriť zálohu CSV súboru každých "backup_interval" iterácií
        if os.path.exists(csv_file) and loop_counter % backup_interval == 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.csv")
            shutil.copy(csv_file, backup_file)
            with open(log_path, "a") as log:
                log.write(f"{datetime.now()}: 🔒 Záloha vytvorená: {backup_file}\n")

    except Exception as e:
        error_message = f"{datetime.now()}: ❌ Chyba pri spúšťaní notebooku: {e}"
        print(error_message)
        with open(log_path, "a") as log:
            log.write(error_message + "\n")
        time.sleep(5)  # ⏱️ 5 sekúnd pred ďalším pokusom

    time.sleep(execution_interval)
    loop_counter += 1
