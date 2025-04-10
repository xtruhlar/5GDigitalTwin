import pandas as pd
import time
import subprocess
import threading
from datetime import datetime, timedelta
import argparse

# === ARGPARSE ===
parser = argparse.ArgumentParser(description="Mirror UE behavior from CSV.")
parser.add_argument('--file', type=str, required=True, help='Path to the CSV file to read UE schedule from.')
args = parser.parse_args()

CSV_PATH = args.file
UE_CONTAINERS = ["nr-ue1.yaml", "nr-ue2.yaml", "nr-ue3.yaml", "nr-ue4.yaml", "nr-ue5.yaml", "nr-ue6.yaml", "nr-ue7.yaml", "nr-ue8.yaml", "nr-ue9.yaml", "nr-ue10.yaml"]
CHECK_INTERVAL = 5  # seconds between events (if not syncing to timestamps)
HOURS_BACK = 0 # how many hours back to consider for simulation

# === LOAD TIMELINE ===
print("📥 Loading simulation data...")
df = pd.read_csv(CSV_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
print(f"✅ Loaded {len(df)} records from {CSV_PATH}\n")

# Keep only future timestamps relative to now
start_time = datetime.now() - timedelta(hours=HOURS_BACK)
df = df[df["timestamp"] >= start_time]

# === UTILS ===

def get_running_ues():
    """Returns list of running UE container names (by YAML)."""
    print("🔍 Checking currently running UE containers...")
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    running = []
    for yaml in UE_CONTAINERS:
        name = yaml.split('.')[0].replace('-', '_')
        if name in result.stdout:
            running.append(yaml)
    print(f"⚙️ Currently running UEs: {len(running)} → {running}")
    return running

def start_ue(index):
    """Start a UE container by its index in the list."""
    if index < len(UE_CONTAINERS):
        yaml = f"nr-UEs/{UE_CONTAINERS[index]}"
        print(f"🚀 Starting container: {yaml}")
        subprocess.run(["docker", "compose", "-f", yaml, "-p", "implementation", "up", "--build", "-d"])
    else:
        print(f"❌ Cannot start UE {index+1}: no such container defined.")

def threaded_stop_ue(yaml):
    """Stop a UE container using threads."""
    print(f"🛑 Stopping container: {yaml}")
    subprocess.run(["docker", "compose", "-f", yaml, "down"])
    print(f"✅ Container stopped: {yaml}")

def stop_ue(index):
    """Stop a UE container by its index in the list, using thread."""
    if index < len(UE_CONTAINERS):
        yaml = UE_CONTAINERS[index]
        t = threading.Thread(target=threaded_stop_ue, args=(yaml,))
        t.start()
        t.join(timeout=8)
        print(f"\n🧵 Thread completed or timed out for stopping {yaml}")
    else:
        print(f"❌ Cannot stop UE {index+1}: no such container defined.")

def sync_to_shadow(target_ues):
    print(f"📡 Target number of UEs: {target_ues}")
    running = get_running_ues()
    current = len(running)
    delta = target_ues - current
    print(f"📈 Delta = {delta} (current: {current}, desired: {target_ues})")

    if delta > 0:
        print(f"➕ Need to start {delta} UE(s)")
        for i in range(current, current + delta):
            start_ue(i)
    elif delta < 0:
        print(f"➖ Need to stop {-delta} UE(s)")
        for i in reversed(range(target_ues, current)):
            stop_ue(i)
    else:
        print("✅ UE count matches desired state. No action needed.")

    print("---")

# === MAIN LOOP ===
print("🔁 Starting Digital Shadow simulation...\n")

for i, row in df.iterrows():
    target_time = row["timestamp"]
    # Last hour
    now = datetime.now() - timedelta(hours=HOURS_BACK)

    if now < target_time:
        sleep_time = (target_time - now).total_seconds()
        print(f"🕒 Waiting {sleep_time:.1f}s to reach event timestamp {target_time}")
        time.sleep(sleep_time)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    active_ues = int(row["Active UEs"])

    print(f"\n⏳ [{current_time}] Event {i+1}/{len(df)} → Desired Active UEs: {active_ues}")
    sync_to_shadow(active_ues)

print("✅ Finished processing all events. Shadow is now aligned with simulated behavior.")
