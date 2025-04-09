import random
import time
from datetime import datetime

sleep_time = 0.1
cooldown_after_anomaly = 5  # Insert at least 1 normal after each anomaly

normal_duration_agg = 0
anomaly_duration_agg = 0

uc_min_durations = {
    "uc_normal_1": 270,
    "uc_normal_2": 334,
    "uc_normal_3": 318,
    "uc_normal_4": 230,
    "uc_normal_5": 324,
    "uc_normal_6": 305,
    "uc_ddos_1": 837,
    "uc_ddos_2": 96
}


# Define scenario pool and split by type
scenario_pool = [
    {
        "id": "uc_normal_1", "type": "normal", "ues": (0, 25), "duration": (270, 300), "data": (10, 200), "burst": False, "script": "uc1_random_load.sh"
    },
    {
        "id": "uc_normal_2", "type": "normal", "ues": (5, 15), "duration": (334, 1800), "data": (0, 0), "burst": False, "script": "uc2_keep_alive.sh"
    },
    {
        "id": "uc_normal_3", "type": "normal", "ues": (20, 40), "duration": (318, 400), "data": (5, 50), "burst": False, "script": "uc3_morning_rush.sh"
    },
    {
        "id": "uc_normal_4", "type": "normal", "ues": (10, 20), "duration": (230, 600), "data": (100, 500), "burst": False, "script": "uc4_evening_streaming.sh"
    },
    {
        "id": "uc_normal_5", "type": "normal", "ues": (10, 10), "duration": (324, 324), "data": (0, 0), "burst": False, "script": "uc5_bg_activity.sh"
    },
    {
        "id": "uc_normal_6", "type": "normal", "ues": (1, 1), "duration": (305, 305), "data": (0, 0), "burst": False, "script": "uc6_night_mode.sh"
    },
    {
        "id": "uc_ddos_1", "type": "ddos", "ues": (200, 200), "duration": (837, 837), "data": (0, 0), "burst": False, "script": "uc7_slow_ddos.sh"
    },
    {
        "id": "uc_ddos_2", "type": "ddos", "ues": (30, 50), "duration": (96, 300), "data": (200, 500), "burst": True, "script": "uc8_traffic_burst.sh"
    },
    {
        "id": "uc_sys_error", "type": "error", "ues": (10, 30), "duration": (200, 300), "data": (0, 0), "burst": False, "script": "stop_all_ues.sh"
    },
]

normal_scenarios = [s for s in scenario_pool if s["type"] == "normal"]
anomaly_scenarios = [s for s in scenario_pool if s["type"] in ["ddos", "error"]]

NORMAL_RATIO = 0.8
ANOMALY_RATIO = 0.2

normal_cycle = int(NORMAL_RATIO * 100)
anomaly_cycle = int(ANOMALY_RATIO * 100)

scenario_sequence = ["normal"] * normal_cycle + ["anomaly"] * anomaly_cycle
random.shuffle(scenario_sequence)

cooldown = False
anomaly_count = 0
normal_count = 0
iteration_count = 0

def run_scenario(scenario):
  global normal_duration_agg, anomaly_duration_agg 
  ues = random.randint(*scenario["ues"])
  duration = random.randint(*scenario["duration"])
  data_volume = random.randint(*scenario["data"])

  normal_duration_agg += duration if scenario["type"] == "normal" else 0
  anomaly_duration_agg += duration if (scenario["type"] == "ddos" or scenario["type"] == "error") else 0

  print("\033[H\033[J", end="")  # Clear the terminal
  print(f"▶️ Running scenario {scenario['id']} at {datetime.now().isoformat()}")
  print(f"   - Type: {scenario['type']}")
  print(f"   - UEs: {ues}")
  print(f"   - Duration: {duration} seconds")
  print(f"   - Data Volume: {data_volume} MB")
  print(f"   - Burst: {scenario['burst']}")
  print(f"   - Script: {scenario['script']}")

  print(f"   ✅ Normal scenarios: {normal_count}")
  print(f"   ⚠️ Anomaly scenarios: {anomaly_count}\n")
  print(f"   📊 {anomaly_count/iteration_count:.2%} anomalies")
  # Time in HH:MM:SS of normal scenarios
  print(f"   ⏳ Normal duration: {normal_duration_agg//3600}:{(normal_duration_agg%3600)//60}:{normal_duration_agg%60}")
  # Time in HH:MM:SS of anomaly scenarios
  print(f"   ⏳ Anomalies duration: {anomaly_duration_agg//3600}:{(anomaly_duration_agg%3600)//60}:{anomaly_duration_agg%60}")
  
  with open("executed_scenarios.csv", "a") as f:
    f.write(f"{datetime.now().isoformat()}, {scenario['id']}, duration={duration}\n")

  time.sleep(sleep_time)  # simulate duration


if __name__ == "__main__":
  while True:
    for label in scenario_sequence:
      iteration_count += 1
      if cooldown:
        print("🧊 Cooldown: Forcing normal scenario after anomaly")
        label = "normal"
        cooldown = False

      if label == "normal":
        selected = random.choice(normal_scenarios)
        normal_count += 1
      else:
        selected = random.choice(anomaly_scenarios)
        anomaly_count += 1
        cooldown = True

      run_scenario(selected)
      time.sleep(sleep_time)

    random.shuffle(scenario_sequence)  # shuffle again for next round
